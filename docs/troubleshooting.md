# 故障排查

## 1. 安装失败

- 检查 Python 版本：`python --version` ≥ 3.11。
- 检查 `pip`：`pip --version`。
- 重装：`pip install -e .[dev]`，查看 traceback。

## 2. 解析失败

- `PDFParseError`：所有 PDF 解析后端均失败。
  - 安装 `pymupdf`、`pypdf`、`pdfplumber`。
  - 检查 PDF 是否加密。
  - 尝试先用 `qpdf --decrypt input.pdf output.pdf` 解密。
- 解析得到 0 字符：
  - PDF 是扫描版。运行 `python -m bookmind.cli analyze ... --enable-ocr`。
  - 安装 OCR：`pip install pytesseract ocrmypdf` + 系统 tesseract。

## 3. 目录识别失败

- 输出 `toc_source=inferred` + `confidence=0.3`：未找到任何章节标题。
  - 检查 PDF 是否扫描版。
  - 检查 PDF 前几页是否被 PDF 阅读器加过"封面"。

## 4. 索引失败

- `OperationalError: no such table: chunks_fts`：
  - 重新运行 `book-deep-reading` 触发 `pipeline.indexer.build_index`。
- 索引查询返回空：
  - 检查 query 是否包含停用词。
  - 改写问题。

## 5. 导出失败

- `weasyprint` 报错：缺系统库。`apt install libcairo2 libpango-1.0-0`。
- HTML 渲染为占位：缺 `markdown` 库。`pip install markdown`。

## 6. 路径错误

- `SecurityError: 路径不在白名单内`：
  - 检查 `.env` 中的 `safe_path_roots`。
  - 用 `python -m bookmind.cli doctor` 看实际配置。

## 7. 性能

- 500 页的 PDF 通常 1–3 分钟出报告（无 LLM 介入）。
- 加 LLM 介入后，章节摘要耗时显著增加，建议异步 + 批量。

## 8. 缓存清理

- `python -m bookmind.cli clean-cache --yes`。

## 9. 升级

- `pip install -U -e .[dev]`。
- 关注 SKILL.md `version` 字段变化。

## 10. 反馈

- 提 issue 请附：
  - `doctor` 输出
  - 报错 traceback
  - PDF 特征（页数、是否扫描、是否加密、是否带目录）
  - 不含版权内容的最小复现命令
