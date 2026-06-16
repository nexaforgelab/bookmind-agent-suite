# OpenClaw Usage Examples

## å®è£

```bash
git clone <repo> bookmind-agent-suite
cd bookmind-agent-suite
./install_openclaw.sh
```

## è°ç¨

### éè¿ slash command

```bash
openclaw agent --message "/book-deep-reading /path/to/book.pdf --mode deep --goal éè¯çè§£"
```

### éè¿èªç¶è¯­è¨

```text
/book-deep-reading æè¿ä¸ä¼ çPDFï¼å¸®æåä¸å®¶çº§è§£è¯»
```

### éè¿ per-agent workspace

`book-reader` agent çæå°éç½®ï¼

```yaml
agents:
  - agentId: book-reader
    workspace: ~/.openclaw/workspace-bookmind
    skills:
      - bookmind/book-deep-reading
      - bookmind/book-pdf-ingest
      - bookmind/book-ocr-cleanup
      - bookmind/book-toc-detect
      - bookmind/book-chapter-summarize
      - bookmind/book-concept-map
      - bookmind/book-critical-analysis
      - bookmind/book-qa
      - bookmind/book-notes-export
      - bookmind/book-review-cards
    sandbox: all
    deny:
      - /etc
      - /var
      - /sys
      - /proc
```

## é£ä¹¦ / å¾®ä¿¡ / Telegram éæ

```python
# pseudo code - ç½å³æ¶å° PDF éä»¶åï¼
import shutil
from pathlib import Path

uploads = Path("~/.openclaw/workspace-bookmind/uploads").expanduser()
uploads.mkdir(parents=True, exist_ok=True)
shutil.copy(attachment_path, uploads / attachment_name)

# ç¶åè§¦åï¼
# /book-deep-reading æè¿ä¸ä¼ çPDF --mode deep --goal éè¯çè§£
```

## è¾åºæä»¶

`~/.openclaw/workspace-bookmind/reports/`

- `*.report.md` â ä¸»æ¥å
- `*.report.html` â ç½é¡µç
- `*.insight.json` â ç»æåæ°æ®
- `*.mindmap.mmd` â Mermaid æç»´å¯¼å¾
- `*.anki.csv` â Anki å¡ç
- `*.evidence.csv` â è¯æ®è¡¨
- `*.obsidian/` â Obsidian vault
