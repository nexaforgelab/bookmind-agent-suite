#!/usr/bin/env python3
"""scripts/run_critical_analysis.py"""
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
        print(__doc__ or "book-critical-analysis: critical analysis")
        print("Usage: run_critical_analysis.py <path/to/book.pdf> [--mode expert]")
        sys.exit(0 if args and args[0] in ("-h", "--help") else 1)
    print(json.dumps(execute_skill("book-critical-analysis", args), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
