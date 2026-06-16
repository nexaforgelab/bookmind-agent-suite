# 安全与商用边界

## 1. 版权

- BookMind 默认不输出大段原文。
- 短引用必须 ≤ `max_quote_words` (默认 60 词) 并带页码。
- 概念解释、章节摘要、应用方案都基于"分析"而非"复制"。
- 不在 `book_insight.json` 中存储完整原文（仅 hash + 切片）。
- 缓存中的 `parsed_book.json` 是中间结果，建议放在用户本地目录。

## 2. 数据驻留

- 默认所有产物保存在本地：
  - `BOOKMIND_OUTPUT_DIR` 默认 `~/BookMind/reports`
  - `BOOKMIND_CACHE_DIR` 默认 `~/.bookmind/cache`
- 如果用户使用云端模型服务，原始 PDF 可能随请求被发送给该服务。
  BookMind 不内置云调用，仅在用户自行接入 LLM 时才会发送。
- 不向任何 BookMind 自己的服务器上传。

## 3. 路径安全

- `PathGuard` 强制路径必须位于 `safe_path_roots`（默认 `~`、`/tmp`）。
- `deny_path_patterns` 禁止读取系统敏感目录（`/etc`, `/var`, `/sys`, `/proc`, `.ssh` 等）。
- 任何外部命令调用都通过 `CommandAllowlist`。

## 4. 解析安全

- 不执行 PDF 内嵌脚本。
- 限制单文件大小（默认 500MB）。
- 限制单文档页数（可在 settings 调整）。
- 对 OCR 输出做大小限制。

## 5. 报告可追溯

- 所有引用必须带 `chapter_id` 或 `page_start`。
- 引用 `quote` 字段长度受限。
- `quality_report.json` 记录每个维度的分数，便于人工审计。

## 6. 商用建议

- 部署到生产环境时：
  - 关闭公网可写的 uploads 目录。
  - 启用 OS 级沙箱（OpenClaw sandbox=all）。
  - 给 OpenClaw agent 设置 `deny` 列表，禁止写系统目录。
  - 把缓存目录放在加密磁盘。
- 用户协议中应明确：
  - 用户对其上传的 PDF 拥有合法使用权。
  - BookMind 仅做摘要 / 分析 / 笔记生成。
  - 用户不得用本工具从事任何侵权用途。

## 7. 已知限制

- PDF 加密 / 数字签名时无法直接解析。
- 扫描版 PDF 需要安装 OCR 依赖。
- 极度复杂的版式（双栏 + 脚注 + 边栏）可能影响分块质量。
- 超大书（> 1000 页）需要分批处理，BookMind 的章节级处理可以缓解。
