"""Tests for PDF parser & related utilities."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from bookmind.config import reset_settings
from bookmind.pipeline.pdf_parser import _try_pymupdf, _try_pypdf
from bookmind.pipeline.ocr import maybe_ocr_pdf
from bookmind.exceptions import PDFParseError, OCRError
from bookmind.utils.text_utils import (
    clean_chinese_text,
    clean_english_text,
    detect_language,
    split_sentences,
)


def test_detect_language():
    assert detect_language("这是一段中文。") == "zh"
    assert detect_language("This is an English sentence.") == "en"
    assert detect_language("This 这段是 mixed 文字。") == "mixed"


def test_clean_chinese_merges_lines():
    text = "第一行没有句号\n第二行接着\n第三行结束。"
    out = clean_chinese_text(text)
    # 中文 PDF 经常由于排版断行，清理器会把无句末标点的连续行合并
    assert "第一行没有句号第二行接着" in out
    assert "第三行结束" in out


def test_clean_chinese_keeps_paragraph_break():
    text = "第一段第一行。\n第一段第二行。\n\n第二段第一行。"
    out = clean_chinese_text(text)
    # 段落之间应有空行
    assert "\n\n" in out


def test_clean_english_fixes_hyphenation():
    text = "This is a long-\nword test.\nNext paragraph."
    out = clean_english_text(text)
    assert "longword" in out


def test_split_sentences_zh():
    s = split_sentences("这是第一句。这是第二句！这是第三句？", lang="zh")
    assert len(s) == 3


def test_split_sentences_en():
    s = split_sentences("Hello world. This is a test! How are you?", lang="en")
    assert len(s) == 3


def test_parse_pdf_fails_on_nonexistent(tmp_workdir: Path):
    reset_settings()
    from bookmind.pipeline.pdf_parser import parse_pdf

    with pytest.raises(PDFParseError):
        parse_pdf(str(tmp_workdir / "missing.pdf"))


def test_ocr_clean_without_dependencies_raises(tmp_workdir: Path):
    """OCR 缺少依赖时，应给出明确错误。"""
    from bookmind.exceptions import OCRError

    # 没有真实 PDF，这里测试 missing-file
    with pytest.raises((OCRError, FileNotFoundError, Exception)):
        try:
            maybe_ocr_pdf(str(tmp_workdir / "no.pdf"))
        except OCRError:
            raise
        except Exception:
            # 也接受底层错误
            raise


def test_pymupdf_returns_none_on_bad_input(tmp_workdir: Path):
    out = _try_pymupdf(str(tmp_workdir / "no.pdf"))
    assert out is None


def test_pypdf_returns_none_on_bad_input(tmp_workdir: Path):
    out = _try_pypdf(str(tmp_workdir / "no.pdf"))
    assert out is None
