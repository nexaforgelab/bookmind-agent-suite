# BookMind Multi-Agent Reading Suite

> **书脑·整本书深度解读多智能体** — 一个可商用的整本书深度解读多 Agent 系统，专为 OpenClaw 和 Hermes 设计。

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-10-purple)](skills/)
[![Agents](https://img.shields.io/badge/agents-13-orange)](bookmind/agents/)

BookMind 是一个 Skill-first 的多智能体系统，把一本 PDF 图书自动拆解为：

- 全书结构与逻辑主线
- 章节摘要与核心问题
- 概念词典与论证图谱
- 批判性分析
- 面向读者目标的可执行方案
- 读书笔记、复习卡片、思维导图
- 多格式导出（Markdown / HTML / JSON / Anki / Obsidian / Mermaid）

## 核心特性

- **多 Agent 协作**：13 个专职 Agent，分工明确，质量可审计
- **Skill-first 架构**：每个能力都是独立可分发的 Skill，符合 OpenClaw / Hermes 标准
- **版权安全**：默认只做摘要、短引用、观点提炼，所有引用带页码
- **长文档友好**：分块、章节处理、上下文压缩、断点续跑

## 阅读模式

- 快速阅读
- 深度阅读
- 主题研读
- 考试/教学定制

## 读者目标

- 知识获取
- 写作借鉴
- 决策支持
- 教学/课程
- 考试冲刺
- 应用迁移
- 内容再生产
- 批判审视
- ...（可在 `bookmind/models.py` 中扩展）

## 导出格式

- Markdown 报告
- HTML 单文件
- JSON 结构化
- Anki 卡片 CSV
- Obsidian 双链
- Mermaid 思维导图
- 短引用清单
- 学术引文

## 快速开始

```bash
pip install -e .
bookmind --help
```

## 文档

- [架构说明](docs/architecture.md)
- [Skill 设计](docs/skill_design.md)
- [商业使用](docs/commercial_usage.md)
- [安全说明](docs/security.md)
- [故障排查](docs/troubleshooting.md)

## 许可

Apache License 2.0