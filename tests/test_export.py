"""Tests for export pipeline."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from bookmind.config import reset_settings
from bookmind.models import (
    BookInsight,
    BookMetadata,
    BookStructure,
    Chapter,
    QualityReport,
)
from bookmind.pipeline.export import export_book_insight


def _make_insight() -> BookInsight:
    return BookInsight(
        metadata=BookMetadata(title="测试书", author="作者", total_pages=10),
        structure=BookStructure(
            title="测试书",
            chapters=[Chapter(chapter_id="ch001", title="第一章", page_start=1, page_end=5, word_count=100)],
        ),
        executive_summary="这是执行摘要。",
        core_thesis="这是核心论点。",
        mindmap_mermaid="mindmap\n  root((测试书))\n    第一章",
        review_cards=[],
        follow_up_questions=["问题 1?", "问题 2?"],
        quality_report=QualityReport(score=90.0, dimensions={}),
    )


def test_export_json(tmp_workdir: Path):
    reset_settings()
    insight = _make_insight()
    out_dir = tmp_workdir / "out"
    res = export_book_insight(insight, out_dir, formats=["json"])
    paths = [p for p in res.paths if p.suffix == ".json"]
    assert paths, "should produce a JSON file"
    # 验证 JSON 可被反序列化
    data = json.loads(paths[0].read_text(encoding="utf-8"))
    assert "metadata" in data


def test_export_markdown(tmp_workdir: Path):
    reset_settings()
    insight = _make_insight()
    out_dir = tmp_workdir / "out"
    res = export_book_insight(insight, out_dir, formats=["markdown"])
    md = next(p for p in res.paths if p.suffix == ".md")
    text = md.read_text(encoding="utf-8")
    assert "测试书" in text
    assert "执行摘要" in text or "核心论点" in text


def test_export_mermaid(tmp_workdir: Path):
    reset_settings()
    insight = _make_insight()
    out_dir = tmp_workdir / "out"
    res = export_book_insight(insight, out_dir, formats=["mermaid"])
    mmd = next(p for p in res.paths if p.suffix == ".mmd")
    assert "mindmap" in mmd.read_text(encoding="utf-8")
