# æéææ¥

## 1. å®è£å¤±è´¥

- æ£æ¥ Python çæ¬ï¼`python --version` â¥ 3.11ã
- æ£æ¥ `pip`ï¼`pip --version`ã
- éè£ï¼`pip install -e .[dev]`ï¼æ¥ç tracebackã

## 2. è§£æå¤±è´¥

- `PDFParseError`ï¼ææ PDF è§£æåç«¯åå¤±è´¥ã
  - å®è£ `pymupdf`ã`pypdf`ã`pdfplumber`ã
  - æ£æ¥ PDF æ¯å¦å å¯ã
  - å°è¯åç¨ `qpdf --decrypt input.pdf output.pdf` è§£å¯ã
- è§£æå¾å° 0 å­ç¬¦ï¼
  - PDF æ¯æ«æçãè¿è¡ `python -m bookmind.cli analyze ... --enable-ocr`ã
  - å®è£ OCRï¼`pip install pytesseract ocrmypdf` + ç³»ç» tesseractã

## 3. ç®å½è¯å«å¤±è´¥

- è¾åº `toc_source=inferred` + `confidence=0.3`ï¼æªæ¾å°ä»»ä½ç« èæ é¢ã
  - æ£æ¥ PDF æ¯å¦æ«æçã
  - æ£æ¥ PDF åå é¡µæ¯å¦è¢« PDF éè¯»å¨å è¿"å°é¢"ã

## 4. ç´¢å¼å¤±è´¥

- `OperationalError: no such table: chunks_fts`ï¼
  - éæ°è¿è¡ `book-deep-reading` è§¦å `pipeline.indexer.build_index`ã
- ç´¢å¼æ¥è¯¢è¿åç©ºï¼
  - æ£æ¥ query æ¯å¦åå«åç¨è¯ã
  - æ¹åé®é¢ã

## 5. å¯¼åºå¤±è´¥

- `weasyprint` æ¥éï¼ç¼ºç³»ç»åºã`apt install libcairo2 libpango-1.0-0`ã
- HTML æ¸²æä¸ºå ä½ï¼ç¼º `markdown` åºã`pip install markdown`ã

## 6. è·¯å¾éè¯¯

- `SecurityError: è·¯å¾ä¸å¨ç½ååå`ï¼
  - æ£æ¥ `.env` ä¸­ç `safe_path_roots`ã
  - ç¨ `python -m bookmind.cli doctor` çå®ééç½®ã

## 7. æ§è½

- 500 é¡µç PDF éå¸¸ 1â3 åéåºæ¥åï¼æ  LLM ä»å¥ï¼ã
- å  LLM ä»å¥åï¼ç« èæè¦èæ¶æ¾èå¢å ï¼å»ºè®®å¼æ­¥ + æ¹éã

## 8. ç¼å­æ¸ç

- `python -m bookmind.cli clean-cache --yes`ã

## 9. åçº§

- `pip install -U -e .[dev]`ã
- å³æ³¨ SKILL.md `version` å­æ®µååã

## 10. åé¦

- æ issue è¯·éï¼
  - `doctor` è¾åº
  - æ¥é traceback
  - PDF ç¹å¾ï¼é¡µæ°ãæ¯å¦æ«æãæ¯å¦å å¯ãæ¯å¦å¸¦ç®å½ï¼
  - ä¸å«çæåå®¹çæå°å¤ç°å½ä»¤
