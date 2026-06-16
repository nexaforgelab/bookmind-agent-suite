"""PDF 解析：优先 PyMuPDF，失败 fallback pypdf。"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..exceptions import PDFParseError
from ..logging_config import get_logger
from ..models import BookMetadata, ParsedBook, ParsedPage, PDFType
from ..utils.text_utils import clean_chinese_text, clean_english_text, detect_language

log = get_logger("pipeline.pdf_parser")

_HEADING_HINT_RE_ZH = re.compile(
    r"^(第[\s\d一二三四五六七八九十百千零〇两]+[章节讲篇回部卷集]|序|前言|引言|后记|附录|参考文献|目\s*录)"
)
_HEADING_HINT_RE_EN = re.compile(
    r"^(chapter|part|section|introduction|conclusion|appendix|references|preface|foreword)\b",
    re.IGNORECASE,
)


def _try_pymupdf(file_path: str) -> Optional[ParsedBook]:
    try:
        import fitz
    except Exception:
        return None
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        log.warning("PyMuPDF 打开失败: {}", e)
        return None

    pages: List[ParsedPage] = []
    toc_raw: List[Dict[str, Any]] = []
    md = doc.metadata or {}
    title = (md.get("title") or Path(file_path).stem).strip()
    author = (md.get("author") or "").strip() or None
    language = "zh-CN"
    full_text = ""

    try:
        toc = doc.get_toc(simple=True)
        for level, t, p in toc:
            toc_raw.append({"level": int(level), "title": t, "page": int(p)})
    except Exception as e:
        log.debug("PyMuPDF 读取 TOC 失败: {}", e)

    for idx, page in enumerate(doc):
        page_no = idx + 1
        try:
            text = page.get_text("text") or ""
        except Exception:
            text = ""
        full_text += "\n" + text

        blocks: List[Dict[str, Any]] = []
        headings: List[str] = []
        try:
            page_dict = page.get_text("dict") or {}
            for blk in page_dict.get("blocks", []):
                if blk.get("type", 0) != 0:
                    continue
                for line in blk.get("lines", []):
                    spans = line.get("spans", [])
                    line_text = "".join(sp.get("text", "") for sp in spans)
                    if not line_text.strip():
                        continue
                    sizes = [sp.get("size", 0) for sp in spans]
                    flags = [sp.get("flags", 0) for sp in spans]
                    bold = any((f & 16) for f in flags)
                    blocks.append({
                        "text": line_text,
                        "size_max": max(sizes) if sizes else 0,
                        "bold": bool(bold),
                        "bbox": blk.get("bbox"),
                    })
                    if max(sizes or [0]) >= 13 or bold or _HEADING_HINT_RE_ZH.match(line_text.strip()) or _HEADING_HINT_RE_EN.match(line_text.strip()):
                        if len(line_text.strip()) <= 80:
                            headings.append(line_text.strip())
        except Exception as e:
            log.debug("解析 page dict 失败: page={} err={}", page_no, e)

        images_count = 0
        try:
            images_count = len(page.get_images(full=True) or [])
        except Exception:
            pass

        char_density = len(text) / max(page.rect.height, 1.0)
        pages.append(ParsedPage(
            page_number=page_no,
            text=text,
            blocks=blocks,
            headings=headings,
            images_count=images_count,
            tables_hint=False,
            char_density=char_density,
        ))

    avg_density = sum(p.char_density for p in pages) / max(len(pages), 1)
    total_chars = sum(len(p.text) for p in pages)
    if total_chars < 200 and avg_density < 0.05:
        pdf_type = PDFType.SCANNED_PDF
    elif total_chars < 2000:
        pdf_type = PDFType.IMAGE_PDF
    else:
        pdf_type = PDFType.TEXT_PDF

    if detect_language(full_text) == "en":
        language = "en-US"
        for p in pages:
            p.text = clean_english_text(p.text)
    else:
        for p in pages:
            p.text = clean_chinese_text(p.text)

    from .ingest import file_hash

    metadata = BookMetadata(
        title=title,
        author=author,
        language=language,
        total_pages=len(pages),
        detected_type=pdf_type,
        confidence=0.9 if pdf_type == PDFType.TEXT_PDF else 0.6,
    )
    return ParsedBook(
        metadata=metadata,
        pages=pages,
        toc_raw=toc_raw,
        file_hash=file_hash(Path(file_path)),
        parser="pymupdf",
    )


def _try_pypdf(file_path: str) -> Optional[ParsedBook]:
    try:
        from pypdf import PdfReader
    except Exception:
        return None
    try:
        reader = PdfReader(file_path)
    except Exception as e:
        log.warning("pypdf 打开失败: {}", e)
        return None
    pages: List[ParsedPage] = []
    full_text = ""
    for idx, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        full_text += "\n" + text
        headings = []
        for ln in text.splitlines():
            s = ln.strip()
            if _HEADING_HINT_RE_ZH.match(s) or _HEADING_HINT_RE_EN.match(s):
                headings.append(s)
        char_density = len(text) / 800.0
        pages.append(ParsedPage(
            page_number=idx + 1,
            text=clean_chinese_text(text) if detect_language(text) != "en" else clean_english_text(text),
            blocks=[],
            headings=headings,
            images_count=0,
            tables_hint=False,
            char_density=char_density,
        ))
    total_chars = sum(len(p.text) for p in pages)
    pdf_type = PDFType.SCANNED_PDF if total_chars < 200 else PDFType.TEXT_PDF
    md_obj = reader.metadata or {}
    from .ingest import file_hash

    metadata = BookMetadata(
        title=(md_obj.get("/Title") or Path(file_path).stem).strip(),
        author=(md_obj.get("/Author") or None),
        language="zh-CN" if detect_language(full_text) != "en" else "en-US",
        total_pages=len(pages),
        detected_type=pdf_type,
        confidence=0.7 if pdf_type == PDFType.TEXT_PDF else 0.4,
    )
    return ParsedBook(
        metadata=metadata,
        pages=pages,
        toc_raw=[],
        file_hash=file_hash(Path(file_path)),
        parser="pypdf",
    )


def parse_pdf(file_path: str) -> ParsedBook:
    log.info("开始解析 PDF: {}", file_path)
    parsed = _try_pymupdf(file_path)
    if parsed is not None:
        log.info("PyMuPDF 解析完成: pages={}, type={}", len(parsed.pages), parsed.metadata.detected_type.value)
        return parsed
    parsed = _try_pypdf(file_path)
    if parsed is not None:
        log.info("pypdf 解析完成: pages={}", len(parsed.pages))
        return parsed
    raise PDFParseError(f"所有 PDF 解析后端均失败: {file_path}")