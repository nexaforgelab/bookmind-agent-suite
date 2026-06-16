#!/usr/bin/env bash
# uninstall.sh - 卸载 BookMind
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${YELLOW}== 卸载 BookMind ==${NC}"

# 1. OpenClaw
OC_SKILLS="$HOME/.openclaw/skills"
if [ -d "$OC_SKILLS" ]; then
  for d in "$OC_SKILLS"/book-deep-reading "$OC_SKILLS"/book-pdf-ingest \
           "$OC_SKILLS"/book-ocr-cleanup "$OC_SKILLS"/book-toc-detect \
           "$OC_SKILLS"/book-chapter-summarize "$OC_SKILLS"/book-concept-map \
           "$OC_SKILLS"/book-critical-analysis "$OC_SKILLS"/book-qa \
           "$OC_SKILLS"/book-notes-export "$OC_SKILLS"/book-review-cards; do
    [ -e "$d" ] && rm -rf "$d" && echo "removed: $d"
  done
fi

# 2. Hermes
HE_SKILLS="$HOME/.hermes/skills"
if [ -d "$HE_SKILLS" ]; then
  for d in "$HE_SKILLS"/book-deep-reading "$HE_SKILLS"/book-pdf-ingest \
           "$HE_SKILLS"/book-ocr-cleanup "$HE_SKILLS"/book-toc-detect \
           "$HE_SKILLS"/book-chapter-summarize "$HE_SKILLS"/book-concept-map \
           "$HE_SKILLS"/book-critical-analysis "$HE_SKILLS"/book-qa \
           "$HE_SKILLS"/book-notes-export "$HE_SKILLS"/book-review-cards; do
    [ -e "$d" ] && rm -rf "$d" && echo "removed: $d"
  done
fi
[ -e "$HOME/.hermes/skill-bundles/book-reading-suite.yaml" ] && \
  rm -f "$HOME/.hermes/skill-bundles/book-reading-suite.yaml" && \
  echo "removed: book-reading-suite.yaml"

# 3. Python 包
if [ -d "$SCRIPT_DIR/.venv" ]; then
  # shellcheck source=/dev/null
  source "$SCRIPT_DIR/.venv/bin/activate" 2>/dev/null || true
  pip uninstall -y bookmind >/dev/null 2>&1 || true
fi

echo -e "${GREEN}== 卸载完成 ==${NC}"
echo "如果需要同时删除缓存，请手动执行: rm -rf ~/.bookmind"
