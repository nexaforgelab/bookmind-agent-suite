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
        metadata=BookMetadata(title="æµè¯ä¹¦", author="ä½è", total_pages=10),
        structure=BookStructure(
            title="æµè¯ä¹¦",
            chapters=[Chapter(chapter_id="ch001", title="ç¬¬ä¸ç« ", page_start=1, page_end=5, word_count=100)],
        ),
        executive_summary="è¿æ¯æ§è¡æè¦ã",
        core_thesis="è¿æ¯æ ¸å¿è®ºç¹ã",
        mindmap_mermaid="mindmap\n  root((æµè¯ä¹¦))\n    ç¬¬ä¸ç« ",
        review_cards=[],
        follow_up_questions=["é®é¢ 1?", "é®é¢ 2?"],
        quality_report=QualityReport(score=90.0, dimensions={}),
    )


def test_export_json(tmp_workdir: Path):
    reset_settings()
    insight = _make_insight()
    out_dir = tmp_workdir / "out"
    res = export_book_insight(insight, out_dir, formats=["json"])
    paths = [p for p in res.paths if p.suffix == ".json"]
    assert paths, "should produce a JSON file"
    # éªè¯ JSON å¯è¢«ååºåå
    data = json.loads(paths[0].read_text(encoding="utf-8"))
    assert "metadata" in data


def test_export_markdown(tmp_workdir: Path):
    reset_settings()
    insight = _make_insight()
    out_dir = tmp_workdir / "out"
    res = export_book_insight(insight, out_dir, formats=["markdown"])
    md = next(p for p in res.paths if p.suffix == ".md")
    text = md.read_text(encoding="utf-8")
    assert "æµè¯ä¹¦" in text
    assert "æ§è¡æè¦" in text or "æ ¸å¿è®ºç¹" in text


def test_export_mermaid(tmp_workdir: Path):
    reset_settings()
    insight = _make_insight()
    out_dir = tmp_workdir / "out"
    res = export_book_insight(insight, out_dir, formats=["mermaid"])
    mmd = next(p for p in res.paths if p.suffix == ".mmd")
    assert "mindmap" in mmd.read_text(encoding="utf-8")
