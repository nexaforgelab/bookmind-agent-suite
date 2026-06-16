"""Tests for TOC detector."""
from __future__ import annotations

import pytest

from bookmind.models import BookMetadata, ParsedBook, ParsedPage
from bookmind.pipeline.toc_detector import detect_toc


def _make_parsed(toc_raw=None, pages_text=None, total_pages=3) -> ParsedBook:
    pages = []
    for i in range(total_pages):
        pages.append(
            ParsedPage(
                page_number=i + 1,
                text=(pages_text[i] if pages_text else ""),
                blocks=[],
                headings=[],
                images_count=0,
                tables_hint=False,
                char_density=0.0,
            )
        )
    return ParsedBook(
        metadata=BookMetadata(title="测试", total_pages=total_pages),
        pages=pages,
        toc_raw=toc_raw or [],
        file_hash="deadbeef",
    )


def test_detect_embedded_toc():
    parsed = _make_parsed(toc_raw=[
        {"level": 1, "title": "第 1 章 序言", "page": 1},
        {"level": 1, "title": "第 2 章 主体", "page": 5},
    ])
    s = detect_toc(parsed)
    assert s.toc_source.value == "embedded"
    assert len(s.chapters) == 2
    assert s.chapters[0].title.startswith("第 1 章")


def test_detect_inferred_fallback_to_single_chapter():
    parsed = _make_parsed(pages_text=["hello world"] * 3, total_pages=3)
    s = detect_toc(parsed)
    assert s.toc_source.value == "inferred"
    assert len(s.chapters) >= 1


def test_detect_zh_toc_page():
    pages_text = [
        "目录\n第 1 章 序言 ........ 1\n第 2 章 主体 ........ 10",
        "正文",
        "正文",
    ]
    parsed = _make_parsed(pages_text=pages_text, total_pages=3)
    s = detect_toc(parsed)
    assert s.toc_source.value in ("detected", "inferred")
    assert s.confidence > 0
