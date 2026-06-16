"""Tests for chunker."""
from __future__ import annotations

from pathlib import Path

import pytest

from bookmind.models import BookStructure, Chapter
from bookmind.pipeline.chunker import build_chunks
from bookmind.utils.token_utils import count_tokens, split_by_tokens


def test_count_tokens_basic():
    n = count_tokens("hello world")
    assert n > 0


def test_split_by_tokens_basic():
    text = ("这是第一句。这是第二句。这是第三句。这是第四句。这是第五句。") * 5
    chunks = split_by_tokens(text, chunk_size=20, overlap=5)
    assert len(chunks) >= 2


def test_build_chunks_preserves_citations():
    chapters_text = {
        "ch001": "第一段内容。" * 50 + " 第二段。" * 30,
        "ch002": "第二章节。" * 30,
    }
    structure = BookStructure(
        title="Test",
        chapters=[
            Chapter(chapter_id="ch001", title="第一章", page_start=1, page_end=2, word_count=100),
            Chapter(chapter_id="ch002", title="第二章", page_start=3, page_end=4, word_count=80),
        ],
    )
    chunks = build_chunks(chapters_text, structure, chunk_size=50, overlap=10)
    assert chunks
    for c in chunks:
        assert c.hash
        assert c.citations
        assert c.citations[0].chapter_id == c.chapter_id


def test_build_chunks_empty_chapter_skipped():
    structure = BookStructure(
        title="Test",
        chapters=[Chapter(chapter_id="ch001", title="X", page_start=1, page_end=1, word_count=0)],
    )
    chunks = build_chunks({"ch001": ""}, structure)
    assert chunks == []
