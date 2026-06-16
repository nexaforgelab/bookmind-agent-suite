"""Tests for PDF parser & related utilities."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from bookmind.config import reset_settings
from bookmind.pipeline.pdf_parser import _try_pymupddf, _try_pypdf
from bookmind.pipeline.ocr import maybe_ocr_pdf
from bookmind.exceptions import PDFParseError, OCRError
from bookmind.utils.text_utils import (
    clean_chinese_text,
    clean_english_text,
    detect_language,
    split_sentences,
)


def test_detect_language():
    assert detect_language("è¿æ¯ä¸æ®µä¸­æã") == "zh"
    assert detect_language("This is an English sentence.") == "en"
    assert detect_language("This è¿æ®µæ¯ mixed å¥åmã") == "mixed"


def test_clean_chinese_merges_lines():
    text = "ç¬¬ä¸è¡ã\nç¬¬ä¸æ®µç¬¬äºè¡ã\n\nç¬¬ä¸è¡ç»æã"
    out = clean_chinese_text(text)
    # ä¸­æ PDF ç»å¸¸ç±äºæçæ­è¡ï¼æ¸çå¨ä¼ææ å¥æ«æ ç¹çè¿ç»­è¡åå¹¶
    assert "ç¬¬ä¸è¡æ²¡æå¥å·ç¬¬äºè¡æ¥ç" in out
    assert "ç¬¬ä¸è¡ç»æ" in out


def test_clean_chinese_keeps_paragraph_break():
    text = "ç¬¬ä¸æ®µç¬¬ä¸è try:
            maybe_ocr_pdf(str(tmp_workdir / "no.pdf"))
        except OCRError:
            raise
        except Exception:
            # ä¹æ¥ååºå±éè¯¯
            raise


def test_pymupdf_returns_none_on_bad_input(tmp_workdir: Path):
    out = _try_pymupddf(str(tmp_workdir / "no.pdf"))
    assert out is None


def test_pypdf