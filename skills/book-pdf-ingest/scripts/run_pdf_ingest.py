#!/usr/bin/env python3
"""scripts/run_pdf_ingest.py - PDF 解析入口。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from bookmind.logging_config import configure_logging
from bookmind.skills_runtime.skill_executor import execute_skill


def main():
    configure_logging()
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__ or "book-pdf-ingest: ingest a PDF book")
        print("Usage: run_pdf_ingest.py <path/to/book.pdf> [options]")
        sys.exit(0 if args and args[0] in ("-h", "--help") else 1)
    result = execute_skill("book-pdf-ingest", args)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
