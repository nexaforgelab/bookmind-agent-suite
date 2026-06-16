#!/usr/bin/env python3
"""scripts/run_qa.py"""
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
    if len(args) < 2:
        print("usage: run_qa.py <index.sqlite> <question>")
        sys.exit(1)
    print(json.dumps(execute_skill("book-qa", args), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
