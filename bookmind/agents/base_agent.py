"""Agent 基类。

每个 Agent 都应该有：
- name：Agent 名
- description：职责
- run(input) -> output：同步执行
- aclose()：可选清理
"""
from __future__ import annotations

import abc
import time
import traceback
from typing import Any, Dict, List, Optional

from ..exceptions import AgentError
from ..logging_config import get_logger
from ..models import AgentInput, AgentOutput


class BaseAgent(abc.ABC):
    name: str = "base"
    description: str = ""

    def __init__(self, name: Optional[str] = None, **kwargs: Any):
        self.name = name or self.name
        self.log = get_logger(f"agent.{self.name}")
        self._kwargs = kwargs

    @abc.abstractmethod
    def run(self, agent_input: AgentInput) -> AgentOutput:
        """子类实现。"""

    def safe_run(self, agent_input: AgentInput) -> AgentOutput:
        """包装：捕获异常并返回失败结果。"""
        started = time.time()
        try:
            self.log.info("Agent {} 开始执行", self.name)
            out = self.run(agent_input)
            out.data.setdefault("elapsed_sec", round(time.time() - started, 3))
            self.log.success(
                "Agent {} 完成 (elapsed={:.2f}s)", self.name, out.data["elapsed_sec"]
            )
            return out
        except Exception as e:  # noqa: BLE001
            tb = traceback.format_exc(limit=5)
            self.log.error("Agent {} 失败: {}\n{}", self.name, e, tb)
            return AgentOutput(
                success=False,
                data={"error": str(e), "elapsed_sec": round(time.time() - started, 3)},
                message=f"Agent {self.name} failed: {e}",
                warnings=[tb],
            )

    def aclose(self) -> None:
        """子类可重写以释放资源。"""
        return None