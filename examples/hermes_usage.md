# Hermes Usage Examples

## å®è£

```bash
./install_hermes.sh
```

## éæ°å è½½ bundle

```bash
hermes bundles reload
hermes skills list
```

## è°ç¨

### éè¿ skill bundle

```bash
hermes
/book-reading-suite /path/to/book.pdf --mode deep --goal åä¸åºç¨
```

### è°ç¨åä¸ªå­ skill

```bash
/book-pdf-ingest /path/to/book.pdf
/book-toc-detect /path/to/book.pdf
/book-chapter-summarize /path/to/book.pdf --mode deep
/book-concept-map /path/to/book.pdf
/book-critical-analysis /path/to/book.pdf --mode expert
/book-qa /path/to/index.sqlite "ä½èçæ ¸å¿è§ç¹æ¯ä»ä¹ï¼"
/book-notes-export /path/to/book.pdf --export markdown,obsidian,anki
/book-review-cards /path/to/book.pdf
```

## [[as_document]] è¾åº

å¨ Hermes ä¼è¯ä¸­è°ç¨å¥å£èæ¬æ¶ï¼å ä¸ `--as-document`ï¼

```bash
python skills/book-deep-reading/scripts/run_book_deep_reading.py \
  /path/to/book.pdf --mode deep --as-document
```

èæ¬ä¼æå°ï¼

```text
[[as_document: /Users/.../reports/MyBook.report.md]]
```

Hermes ä¼æå®è§£æä¸º"ä½ä¸ºææ¡£è¿å"ã

## å¸è½½

```bash
bash uninstall.sh
```
