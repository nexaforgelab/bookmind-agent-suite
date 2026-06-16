#!/usr/bin/env python3
"""scripts/run_book_deep_reading.py

总入口脚本：可被 Hermes / OpenClaw 通过 `python scripts/run_book_deep_reading.py ...` 调用。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# 让脚本可以直接 `python scripts/run_book_deep_reading.py ...` 运行
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from bookmind.logging_config import configure_logging
from bookmind.skills_runtime.skill_executor import execute_skill


def main():
    configure_logging()
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    # Hermes [[as_document]] 指令透传
    as_document = False
    if "--as-document" in args:
        as_document = True
        args = [a for a in args if a != "--as-document"]

    result = execute_skill("book-deep-reading", args)
    out_dir = (result.get("data") or {}).get("result", {}).get("output_dir")
    report_files = []
    if out_dir:
        for p in sorted(Path(out_dir).glob("*")):
            if p.is_file():
                report_files.append(str(p.resolve()))
    # 打印结果
    summary = {
        "ok": result.get("ok"),
        "type": result.get("type"),
        "output_dir": out_dir,
        "files": report_files,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if as_document and report_files:
        # Hermes 解析 [[as_document]] 会以文件形式返回
        print(f"\n[[as_document: {report_files[0]}]]")


if __name__ == "__main__":
    main()
