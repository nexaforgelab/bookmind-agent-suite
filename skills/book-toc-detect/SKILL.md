---
name: book-toc-detect
description: Detect or infer a book's table of contents. Uses embedded TOC, scans the first pages for "目录"/"Contents", then falls back to heuristic heading detection.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [pdf, toc, structure]
    category: productivity
    requires_toolsets: [terminal]
---

# Book TOC Detect

## When to Use
Use this skill when you need a structured `BookStructure` for a PDF (chapter list, page ranges, TOC source, confidence).

## Procedure
1. Read embedded TOC via PyMuPDF.
2. Scan first 5 pages for "目录" / "Contents" pages and match chapter lines.
3. Fall back to heuristic heading detection (font size, bold, page numbers, regex patterns).
4. Return the best structure with `toc_source` and `confidence`.

## Safety
- Never modify the original PDF.

## Failure Handling
- If no chapters are detected, return a single-chapter structure with `confidence=0.3` and a warning.

## Example
```bash
python skills/book-toc-detect/scripts/run_toc_detect.py /path/to/book.pdf
```
