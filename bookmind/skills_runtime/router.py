"""Skill 路由器。"""
from __future__ import annotations

import re
from typing import List, Optional

from .registry import discover_skills


def match_skill(query: str, top_k: int = 3) -> List[dict]:
    if not query:
        return []
    q = query.lower()
    tokens = set(re.findall(r"[a-z0-9一-鿿]+", q))
    skills = discover_skills()
    scored = []
    for s in skills:
        score = 0.0
        name = s["name"].lower()
        desc = (s.get("description") or "").lower()
        for t in tokens:
            if t in name:
                score += 3
            if t in desc:
                score += 1
        if score > 0:
            scored.append((score, s))
    scored.sort(key=lambda x: -x[0])
    return [s for _, s in scored[:top_k]]