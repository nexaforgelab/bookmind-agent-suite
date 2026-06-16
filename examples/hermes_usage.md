# Hermes Usage Examples

## 安装

```bash
./install_hermes.sh
```

## 重新加载 bundle

```bash
hermes bundles reload
hermes skills list
```

## 调用

### 通过 skill bundle

```bash
hermes
/book-reading-suite /path/to/book.pdf --mode deep --goal 商业应用
```

### 调用单个子 skill

```bash
/book-pdf-ingest /path/to/book.pdf
/book-toc-detect /path/to/book.pdf
/book-chapter-summarize /path/to/book.pdf --mode deep
/book-concept-map /path/to/book.pdf
/book-critical-analysis /path/to/book.pdf --mode expert
/book-qa /path/to/index.sqlite "作者的核心观点是什么？"
/book-notes-export /path/to/book.pdf --export markdown,obsidian,anki
/book-review-cards /path/to/book.pdf
```

## [[as_document]] 输出

在 Hermes 会话中调用入口脚本时，加上 `--as-document`：

```bash
python skills/book-deep-reading/scripts/run_book_deep_reading.py \
  /path/to/book.pdf --mode deep --as-document
```

脚本会打印：

```text
[[as_document: /Users/.../reports/MyBook.report.md]]
```

Hermes 会把它解析为"作为文档返回"。

## 卸载

```bash
bash uninstall.sh
```
