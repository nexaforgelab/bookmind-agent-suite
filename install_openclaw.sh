#!/usr/bin/env bash
# install_openclaw.sh - 在 OpenClaw 中安装 BookMind Skill Suite
# 用法：bash install_openclaw.sh
set -euo pipefail

# ---------- 颜色 ----------
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

info()    { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()      { echo -e "${GREEN}[ OK ]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()     { echo -e "${RED}[FAIL]${NC}  $*"; }

# ---------- 路径 ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
SKILLS_DIR="$OPENCLAW_HOME/skills"
WORKSPACE_DIR="$OPENCLAW_HOME/workspace-bookmind"
UPLOAD_DIR="$WORKSPACE_DIR/uploads"
REPORT_DIR="$WORKSPACE_DIR/reports"

info "BookMind OpenClaw 安装器"
info "  源目录: $SCRIPT_DIR"
info "  目标:   $OPENCLAW_HOME"

# ---------- 1. 检查 Python ----------
if ! command -v python3 >/dev/null 2>&1; then
  err "未找到 python3，请先安装 Python 3.11+"
  exit 1
fi
PY_VERSION=$(python3 -c 'import sys; print("%d.%d" % (sys.version_info[:2]))')
info "Python 版本: $PY_VERSION"
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)'; then
  err "需要 Python 3.11+，当前 $PY_VERSION"
  exit 1
fi

# ---------- 2. 创建目录 ----------
info "创建 OpenClaw 目录结构..."
mkdir -p "$SKILLS_DIR" "$WORKSPACE_DIR" "$UPLOAD_DIR" "$REPORT_DIR"
ok "目录已就绪: $SKILLS_DIR, $WORKSPACE_DIR"

# ---------- 3. 链接 Skill ----------
info "安装 BookMind Skills 到 $SKILLS_DIR ..."
for skill_dir in "$SCRIPT_DIR"/skills/*/; do
  skill_name="$(basename "$skill_dir")"
  target="$SKILLS_DIR/$skill_name"
  if [ -e "$target" ] || [ -L "$target" ]; then
    warn "已存在: $target，删除旧链接/目录"
    rm -rf "$target"
  fi
  ln -s "$skill_dir" "$target"
  ok "  ↳ 链接 $skill_name"
done

# ---------- 4. 安装 Python 包 ----------
info "安装 bookmind Python 包..."
cd "$SCRIPT_DIR"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
# shellcheck source=/dev/null
source .venv/bin/activate
pip install --upgrade pip >/dev/null
pip install -e ".[dev]" || warn "完整安装失败，尝试仅核心依赖"
pip install -e . || err "安装 bookmind 包失败"
ok "bookmind Python 包已安装"

# ---------- 5. 生成 AGENTS.md ----------
AGENTS_MD="$WORKSPACE_DIR/AGENTS.md"
cat > "$AGENTS_MD" <<'EOF'
# BookMind OpenClaw Agent Workspace

这是一个为 BookMind 整本书深度解读系统预配置的 OpenClaw 工作区。

## 可用 Skill
- `book-deep-reading`：总入口，整本书深度解读
- `book-pdf-ingest`：PDF 解析与清洗
- `book-ocr-cleanup`：OCR 兜底
- `book-toc-detect`：目录识别
- `book-chapter-summarize`：章节摘要
- `book-concept-map`：概念图谱
- `book-critical-analysis`：批判性分析
- `book-qa`：基于整本书的问答
- `book-notes-export`：笔记导出
- `book-review-cards`：复习卡片

## 推荐 Agent
- `book-reader`：使用上方所有 Skill，专用于读 PDF

## 常用命令

```bash
# 完整深度解读
/book-deep-reading /path/to/book.pdf --mode deep --goal 通识理解

# 专家级解读 + 多格式导出
/book-deep-reading /path/to/book.pdf --mode expert --goal 投资研究 \
  --export markdown,html,json,obsidian,anki,mermaid

# 基于已上传 PDF 自动定位
/book-deep-reading 最近上传的PDF，帮我做专家级解读
```

## 文件目录
- `uploads/`：上传的原始 PDF
- `reports/`：生成的读书报告
EOF
ok "AGENTS.md 已生成: $AGENTS_MD"

# ---------- 6. 输出使用说明 ----------
cat <<EOF

${GREEN}============================================${NC}
${GREEN}  BookMind OpenClaw 安装完成 ${NC}
${GREEN}============================================${NC}

已安装的 Skills:
$(ls -1 "$SKILLS_DIR" | sed 's/^/  - /')

工作区目录: $WORKSPACE_DIR
  - uploads/   放置待解读的 PDF
  - reports/   生成的报告

调用示例:
  openclaw agent --message "/book-deep-reading \$HOME/.openclaw/workspace-bookmind/uploads/yourbook.pdf --mode deep --goal 通识理解"

或者在聊天中直接发送 PDF 附件，对 Agent 说:
  /book-deep-reading 最近上传的PDF，帮我做专家级解读

Telegram / 飞书 / 微信网关收到 PDF 后建议工作流:
  1) 将附件保存到 uploads/
  2) 调用 /book-deep-reading 最近上传的PDF
  3) 把生成的 report.md / report.html 作为文档返回

卸载:
  bash $SCRIPT_DIR/uninstall.sh

EOF
