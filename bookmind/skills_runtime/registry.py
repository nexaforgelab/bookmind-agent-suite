"""Skills 注册中心。"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml
    _HAS_YAML = True
except Exception:
    _HAS_YAML = False


def _skill_paths() -> List[Path]:
    env = os.environ.get("BOOKMIND_SKILLS_DIR")
    candidates: List[Path] = []
    if env:
        candidates.append(Path(env).expanduser())
    candidates.append(Path(__file__).resolve().parent.parent.parent.parent / "skills")
    candidates.append(Path.cwd() / "skills")
    seen = set()
    out = []
    for c in candidates:
        p = c.resolve()
        if p in seen:
            continue
        seen.add(p)
        if p.exists():
            out.append(p)
    return out


def _read_manifest(p: Path) -> Optional[Dict]:
    for name in ("SKILL.md", "skill.yaml", "skill.yml", "manifest.json"):
        f = p / name
        if f.exists():
            try:
                if name.endswith(".md"):
                    text = f.read_text(encoding="utf-8")
                    return _parse_md_manifest(text)
                if name.endswith((".yaml", ".yml")):
                    if not _HAS_YAML:
                        continue
                    return yaml.safe_load(f.read_text(encoding="utf-8"))
                if name.endswith(".json"):
                    return json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                return None
    return None


def _parse_md_manifest(text: str) -> Dict:
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            block = text[3:end]
            for line in block.splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip()
    return meta


def discover_skills() -> List[Dict]:
    out = []
    seen_names = set()
    for root in _skill_paths():
        for p in sorted(root.iterdir()):
            if not p.is_dir():
                continue
            if p.name.startswith(("_", ".")):
                continue
            meta = _read_manifest(p)
            if not meta:
                continue
            name = meta.get("name") or p.name
            if name in seen_names:
                continue
            seen_names.add(name)
            out.append({
                "name": name,
                "version": meta.get("version", "0.1.0"),
                "description": meta.get("description", ""),
                "path": str(p),
                "meta": meta,
            })
    return out


def load_skill(name: str) -> Optional[Dict]:
    for s in discover_skills():
        if s["name"] == name:
            return s
    return None