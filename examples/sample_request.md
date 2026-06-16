# Sample BookMind Request

这是一个示例：用户上传了一本《思考，快与慢》的 PDF，希望生成深度解读报告。

## 用户输入

```text
/book-deep-reading ~/Books/thinking-fast-and-slow.pdf \
  --mode deep \
  --goal 通识理解 \
  --export markdown,html,json,obsidian,anki,mermaid
```

## 触发流程

1. `book-pdf-ingest` 解析 PDF（PyMuPDF）
2. `book-toc-detect` 识别目录
3. `book-chapter-summarize` 逐章摘要
4. `book-concept-map` 提取概念
5. `book-critical-analysis` 批判性分析
6. `book-notes-export` 生成 Markdown/HTML/Obsidian/Anki
7. `book-review-cards` 生成复习卡片
8. `bookmind.pipeline.export` 渲染最终报告

## 期望输出

```
~/BookMind/reports/思考，快与慢/
├── 思考，快与慢.insight.json
├── 思考，快与慢.report.md
├── 思考，快与慢.report.html
├── 思考，快与慢.mindmap.mmd
├── 思考，快与慢.anki.csv
├── 思考，快与慢.evidence.csv
└── 思考，快与慢.obsidian/
    ├── README.md
    ├── chapters/
    └── concepts/
```

## 自然语言示例

```text
/book-deep-reading 最近上传的PDF，帮我做专家级解读，目标：投资研究
```

BookMind 会自动：

1. 在 workspace 中找到最近上传的 PDF
2. 用 `mode=expert`、`goal=投资研究` 调用
3. 在输出报告中追加 `expert_review.md.j2` 的内容
4. 给出投资研究角度的应用方案
