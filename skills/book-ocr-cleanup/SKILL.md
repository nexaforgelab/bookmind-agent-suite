---
name: book-ocr-cleanup
description: Run OCR on scanned/image PDFs to produce a text PDF. Supports pytesseract and ocrmypdf as optional backends.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [ocr, pdf, scanning]
    category: productivity
    requires_toolsets: [terminal]
---

# Book OCR Cleanup

## When to Use
Use this skill when the user uploads a scanned PDF or an image-based PDF and text density is too low for normal parsing.

## Procedure
1. Confirm OCR dependencies are installed.
2. Prefer `ocrmypdf` if available; otherwise use `pytesseract` + render-to-PDF.
3. Write output PDF and return the path.

## Safety
- Run only allowlisted binaries: `ocrmypdf`, `tesseract`, `pdftotext`, `pdfinfo`, `weasyprint`.
- Avoid network calls.

## Failure Handling
- If no OCR backend is installed, return a structured error explaining how to install one.

## Example
```bash
python skills/book-ocr-cleanup/scripts/run_ocr_cleanup.py /path/to/scanned.pdf --out /path/to/out.pdf
```
