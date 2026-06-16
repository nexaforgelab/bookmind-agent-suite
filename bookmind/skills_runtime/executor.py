"""Skill 执行器。"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from ..logging_config import get_logger

log = get_logger("skills.executor")


def execute_skill(name: str, payload: Dict[str, Any], python: Optional[str] = None) -> Dict[str, Any]:
    from .registry import load_skill

    info = load_skill(name)
    if info is None:
        return {"success": False, "error": f"未找到 skill: {name}"}
    skill_path = Path(info["path"])
    script = skill_path / "scripts" / f"run_{name}.py"
    if not script.exists():
        return {"success": False, "error": f"未找到入口: {script}"}
    py = python or sys.executable
    import json as _json
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        proc = subprocess.run(
            [py, str(script), _json.dumps(payload, ensure_ascii=False)],
            capture_output=True,
            text=True,
            env=env,
            timeout=300,
        )
    except Exception as e:
        return {"success": False, "error": str(e)}
    if proc.returncode != 0:
        return {
            "success": False,
            "error": proc.stderr or "skill failed",
            "stdout": proc.stdout,
        }
    return {
        "success": True,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }