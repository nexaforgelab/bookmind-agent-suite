# OpenClaw Usage Examples

## 安装

```bash
git clone <repo> bookmind-agent-suite
cd bookmind-agent-suite
./install_openclaw.sh
```

## 调用

### 通过 slash command

```bash
openclaw agent --message "/book-deep-reading /path/to/book.pdf --mode deep --goal 通识理解"
```

### 通过自然语言

```text
/book-deep-reading 最近上传的PDF，帮我做专家级解读
```

### 通过 per-agent workspace

`book-reader` agent 的最小配置：

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

## 飞书 / 微信 / Telegram 集成

```python
# pseudo code - 网关收到 PDF 附件后：
import shutil
from pathlib import Path

uploads = Path("~/.openclaw/workspace-bookmind/uploads").expanduser()
uploads.mkdir(parents=True, exist_ok=True)
shutil.copy(attachment_path, uploads / attachment_name)

# 然后触发：
# /book-deep-reading 最近上传的PDF --mode deep --goal 通识理解
```

## 输出文件

`~/.openclaw/workspace-bookmind/reports/`

- `*.report.md` — 主报告
- `*.report.html` — 网页版
- `*.insight.json` — 结构化数据
- `*.mindmap.mmd` — Mermaid 思维导图
- `*.anki.csv` — Anki 卡片
- `*.evidence.csv` — 证据表
- `*.obsidian/` — Obsidian vault
