# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-06-15

### Added
- 13 个专职 Agent：BookDirector / Structure / ChapterSummary / Concept / Argument /
  Evidence / CriticalThinking / DomainApplication / QA / Note / Mindmap / Review / ReportEditor
- 10 个 OpenClaw / Hermes 兼容 Skill：book-deep-reading / book-pdf-ingest /
  book-ocr-cleanup / book-toc-detect / book-chapter-summarize / book-concept-map /
  book-critical-analysis / book-qa / book-notes-export / book-review-cards
- Hermes skill bundle `book-reading-suite.yaml`
- 多 PDF 后端解析：PyMuPDF 优先，pypdf 兜底；可选 pytesseract / ocrmypdf / paddleocr
- 9 档读者目标 × 4 档解读深度 (quick / standard / deep / expert)
- 8 种导出格式：Markdown / HTML / JSON / CSV / Anki CSV / Obsidian Vault /
  Mermaid 思维导图 / 可选 PDF
- SQLite FTS5 索引 + 章节级处理，支持长文档
- 路径白名单 + 命令 allowlist + 短引用裁剪三道安全边界
- Pydantic v2 数据模型
- 中英混排 PDF 支持
- Typer CLI：`analyze` / `ask` / `export` / `doctor` / `clean-cache`
- Docker / docker-compose 一键启动
- 23 个 pytest 单元测试
- CI：GitHub Actions 多平台多版本
- Apache 2.0 License

### Notes
- 默认走启发式摘要；要获得更深度分析，可在 `bookmind/agents/` 下接入 LLM provider
- 缓存目录：`~/.bookmind/cache`；报告目录：`~/BookMind/reports`

[Unreleased]: https://example.com/bookmind/compare/v1.0.0...HEAD
[1.0.0]: https://example.com/bookmind/releases/tag/v1.0.0
