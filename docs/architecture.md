# BookMind 架构

## 总览

BookMind 是 Skill-first 的多 Agent 系统。每个能力都是独立可分发的 Skill，
组合在一起由 `BookDirectorAgent` 调度。

```
┌────────────────────────────────────────────────┐
│  OpenClaw / Hermes / CLI 入口                  │
└──────────────────┬─────────────────────────────┘
                   ▼
        ┌──────────────────────┐
        │   Orchestrator       │
        └──────────┬───────────┘
                   ▼
        ┌──────────────────────┐
        │  BookDirectorAgent   │
        └──────────┬───────────┘
                   ▼
   ┌─────────── 解析 / 切分 / 分块 ─────────────┐
   │  pdf_parser → toc_detector → chapter_segmenter │
   │  chunker → indexer (FTS5) → cache             │
   └──────────────┬─────────────────────────────┘
                  ▼
   ┌──────────── 调度子 Agent ───────────────────┐
   │  structure / chapter_summary / concept / arg │
   │  evidence / critical / domain / notes       │
   │  mindmap / review / report_editor           │
   └──────────────┬─────────────────────────────┘
                  ▼
         ┌──────────────────┐
         │ export (md,html…)│
         └──────────────────┘
```

## 关键设计

### 1. Skill-first
- 每个能力可被 Hermes / OpenClaw 单独调用。
- 入口 Skill `book-deep-reading` 是一个聚合器。

### 2. 数据模型
- Pydantic v2 严格模型。
- 关键实体：`ReadingRequest`, `BookMetadata`, `BookStructure`,
  `BookChunk`, `ChapterInsight`, `BookInsight`, `QualityReport`。

### 3. 流水线
- `pipeline/` 全部为纯 Python 函数，可单独测试。
- `agents/` 把流水线包装为可调度的能力。

### 4. 缓存 / 断点续跑
- 按文件 SHA256 缓存 parsed_book / structure。
- 中间结果以 JSON 落盘，可恢复。

### 5. 安全
- 路径白名单 + 拒绝规则。
- 命令 allowlist。
- 短引用裁剪 + 来源标注。

## 扩展

### 新增 Agent
1. 在 `bookmind/agents/` 下继承 `BaseAgent`。
2. 在 `BookDirectorAgent` 中接入。
3. 写 SKILL.md 并注册到 router。

### 新增 Skill
1. 在 `skills/<skill-name>/` 下写 SKILL.md。
2. 在 `skill_executor.py` 中注册 handler。
3. 在 `skill-bundles/` 中加入 bundle YAML。

### 新增导出格式
1. 在 `pipeline/export.py` 中加分支。
2. 在 `ReadingRequest.export_formats` 的字面量中加值。
