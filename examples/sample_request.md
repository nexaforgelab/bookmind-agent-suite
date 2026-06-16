# Sample BookMind Request

è¿æ¯ä¸ä¸ªç¤ºä¾ï¼ç¨æ·ä¸ä¼ äºä¸æ¬ãæèï¼å¿«ä¸æ¢ãç PDFï¼å¸æçææ·±åº¦è§£è¯»æ¥åã

## ç¨æ·è¾å¥

```text
/book-deep-reading ~/Books/thinking-fast-and-slow.pdf \
  --mode deep \
  --goal éè¯çè§£ \
  --export markdown,html,json,obsidian,anki,mermaid
```

## è§¦åæµç¨

1. `book-pdf-ingest` è§£æ PDFï¼PyMuPDFï¼
2. `book-toc-detect` è¯å«ç®å½
3. `book-chapter-summarize` éç« æè¦
4. `book-concept-map` æåæ¦å¿µ
5. `book-critical-analysis` æ¹å¤æ§åæ
6. `book-notes-export` çæ Markdown/HTML/Obsidian/Anki
7. `book-review-cards` çæå¤ä¹ å¡ç
8. `bookmind.pipeline.export` æ¸²ææç»æ¥å

## ææè¾åº

```
~/BookMind/reports/æèï¼å¿«ä¸æ¢/
âââ æèï¼å¿«ä¸æ¢.insight.json
âââ æèï¼å¿«ä¸æ¢.report.md
âââ æèï¼å¿«ä¸æ¢.report.html
âââ æèï¼å¿«ä¸æ¢.mindmap.mmd
âââ æèï¼å¿«ä¸æ¢.anki.csv
âââ æèï¼å¿«ä¸æ¢.evidence.csv
âââ æèï¼å¿«ä¸æ¢.obsidian/
    âââ README.md
    âââ chapters/
    âââ concepts/
```

## èªç¶è¯­è¨ç¤ºä¾

```text
/book-deep-reading æè¿ä¸ä¼ çPDFï¼å¸®æåä¸å®¶çº§è§£è¯»ï¼ç®æ ï¼æèµç ç©¶
```

BookMind ä¼èªå¨ï¼

1. å¨ workspace ä¸­æ¾å°æè¿ä¸ä¼ ç PDF
2. ç¨ `mode=expert`ã`goal=æèµç ç©¶` è°ç¨
3. å¨è¾åºæ¥åä¸­è¿½å  `expert_review.md.j2` çåå®¹
4. ç»åºæèµç ç©¶è§åº¦çåºç¨æ¹æ¡
