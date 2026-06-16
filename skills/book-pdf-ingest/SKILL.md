---
name: book-pdf-ingest
description: Parse a PDF book with PyMuPDF (preferred) or pypdf fallback. Detect PDF type (text/scanned/image/mixed), language, and clean text. Outputs a parsed book JSON.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [pdf, parsing, ingestion]
    category: productivity
    requires_toolsets: [terminal]
---

# Book PDF Ingest

## When to Use
Use this skill to ingest a PDF book and produce a clean `parsed_book.json`. Pair with `book-toc-detect` and `book-chapter-summarize`.

## Procedure
1. Resolve and validate the file path (must end with `.pdf`).
2. Try `pymupdf` first; if it fails, fall back to `pypdf`.
3. Detect PDF type by character density.
4. Clean Chinese / English text (hyphenation, header / footer removal, line joining).
5. Cache by file hash.

## Safety
- Reject paths outside safe roots.
- Cap file size to prevent OOM.

## Example
```bash
python -m bookmind.cli analyze /path/to/book.pdf --mode quick --export json
```

## Failure Handling
- Encrypted PDF → return error, ask user for decrypted copy.
- Scanned PDF → recommend running with `book-ocr-cleanup` first.
