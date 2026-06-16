"""BookMind Skills Runtime。

负责：
- 解析 OpenClaw / Hermes 调用上下文
- 路由到具体 Skill
- 收集并返回结果
"""
from .skill_context import SkillContext
from .skill_router import SkillRouter

__all__ = ["SkillContext", "SkillRouter"]
