"""StructureAgent - 结构分析。

根据 toc_detector 的输出做精炼、补全缺失信息（出版社、年份、ISBN）。
"""
from __future__ import annotations

import re
from typing import List

from ..logging_config import get_logger
from ..models import AgentInput, AgentOutput, BookStructure
from .base_agent import BaseAgent

log = get_logger("agent.structure")


class StructureAgent(BaseAgent):
    name = "structure"
    description = "结构分析：补全书结构、规范化元数据。"

    def run(self, agent_input: AgentInput) -> AgentOutput:
        parsed = agent_input.parsed_book
        structure: BookStructure = agent_input.structure  # type: ignore[assignment]
        if parsed is None or structure is None:
            return AgentOutput(success=False, message="缺少 parsed_book 或 structure")

        # 补全：尝试从首两页文本中识别 ISBN、出版社、年份
        head_text = "\n".join(p.text for p in parsed.pages[:3])
        if not parsed.metadata.publisher:
            m = re.search(r"([\u4e00-\u9fffA-Za-z ·]{2,30}(?:出版社|Press|publishing|Publishing))", head_text)
            if m:
                parsed.metadata.publisher = m.group(1).strip()
        if not parsed.metadata.publication_year:
            m = re.search(r"(20\d{2}|19\d{2})\s*年?", head_text)
            if m:
                try:
                    parsed.metadata.publication_year = int(m.group(1))
                except ValueError:
                    pass
        if not parsed.metadata.isbn:
            m = re.search(r"ISBN[\s:：]*([\d\-Xx]{10,17})", head_text, re.IGNORECASE)
            if m:
                parsed.metadata.isbn = m.group(1)

        # 规范化章节标题
        for ch in structure.chapters:
            ch.title = re.sub(r"\s+", " ", ch.title).strip()

        # 估算 word_count
        from ..pipeline.chapter_segmenter import segment_chapters

        chapters_text = segment_chapters(parsed, structure)
        for ch in structure.chapters:
            ch.word_count = len(chapters_text.get(ch.chapter_id, ""))

        log.info(
            "Structure 解析: chapters={} publisher={} year={}",
            len(structure.chapters),
            parsed.metadata.publisher,
            parsed.metadata.publication_year,
        )
        return AgentOutput(
            success=True,
            data={
                "metadata": parsed.metadata.model_dump(mode="json"),
                "structure": structure.model_dump(mode="json"),
            },
        )