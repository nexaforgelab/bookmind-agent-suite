#!/usr/bin/env bash
# install_hermes.sh - 在 Hermes 中安装 BookMind Skill Suite
# 用法：bash install_hermes.sh
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

info()    { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()      { echo -e "${GREEN}[ OK ]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()     { echo -e "${RED}[FAIL]${NC}  $*"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
SKILLS_DIR="$HERMES_HOME/skills"
BUNDLES_DIR="$HERMES_HOME/skill-bundles"
BOOKMIND_DIR="$HOME/.bookmind"
WORKSPACE_DIR="$BOOKMIND_DIR/workspace"
UPLOAD_DIR="$WORKSPACE_DIR/uploads"
REPORT_DIR="$WORKSPACE_DIR/reports"

info "BookMind Hermes 安装器"
info "  源目录: $SCRIPT_DIR"
info "  目标:   $HERMES_HOME"

# ---------- 1. 检查 Python ----------
if ! command -v python3 >/dev/null 2>&1; then
  err "未找到 python3，请先安装 Python 3.11+"
  exit 1
fi
PY_VERSION=$(python3 -c 'import sys; print("%d.%d" % (sys.version_info[:2]))')
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)'; then
  err "需要 Python 3.11+，当前 $PY_VERSION"
  exit 1
fi
ok "Python $PY_VERSION"

# ---------- 2. 目录 ----------
info "创建 Hermes 目录结构..."
mkdir -p "$SKILLS_DIR" "$BUNDLES_DIR" "$WORKSPACE_DIR" "$UPLOAD_DIR" "$REPORT_DIR"
ok "目录已就绪"

# ---------- 3. 复制 Skills ----------
info "复制 BookMind Skills 到 $SKILLS_DIR ..."
for skill_dir in "$SCRIPT_DIR"/skills/*/; do
  skill_name="$(basename "$skill_dir")"
  target="$SKILLS_DIR/$skill_name"
  rm -rf "$target"
  cp -R "$skill_dir" "$target"
  ok "  ↳ 安装 $skill_name"
done

# ---------- 4. 复制 skill bundle ----------
info "复制 skill bundle..."
cp -f "$SCRIPT_DIR/skill-bundles/book-reading-suite.yaml" "$BUNDLES_DIR/"
ok "  ↳ book-reading-suite.yaml"

# ---------- 5. 安装 Python 包 ----------
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

# ---------- 6. 生成使用说明 ----------
cat <<EOF

${GREEN}============================================${NC}
${GREEN}  BookMind Hermes 安装完成 ${NC}
${GREEN}============================================${NC}

已安装 Skills:
$(ls -1 "$SKILLS_DIR" | sed 's/^/  - /')

Bundle: book-reading-suite

调用方法:
  hermes
  /book-reading-suite /path/to/book.pdf --mode deep --goal 商业应用

重新加载:
  hermes bundles reload
  hermes skills list

工作区:
  - $UPLOAD_DIR   放置 PDF
  - $REPORT_DIR   报告输出

卸载:
  bash $SCRIPT_DIR/uninstall.sh

EOF
