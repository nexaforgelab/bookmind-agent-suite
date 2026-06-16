#!/usr/bin/env bash
# publish.sh - 一键发布 BookMind 到 GitHub
# 用法:
#   1) 在 GitHub 上先创建一个空仓库（不要勾选 README/license/.gitignore）
#      推荐名: bookmind-agent-suite
#      License: Apache-2.0（也可以先不选，由我们推送 LICENSE）
#   2) 替换下面的 REPO_URL 为你的仓库地址
#   3) bash publish.sh

set -euo pipefail

# ============ 在这里改 ============
REPO_URL="${REPO_URL:-https://github.com/YOUR_ORG/bookmind-agent-suite.git}"
VISIBILITY="${VISIBILITY:-public}"   # public | private
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"
COMMIT_AUTHOR_NAME="${COMMIT_AUTHOR_NAME:-$(git config --get user.name || echo BookMind Authors)}"
COMMIT_AUTHOR_EMAIL="${COMMIT_AUTHOR_EMAIL:-$(git config --get user.email || echo bookmind@example.com)}"
# ===================================

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info() { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()   { echo -e "${GREEN}[ OK ]${NC}  $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC}  $*"; }

cd "$(dirname "$0")"

# 1) 校验
if [ ! -f "LICENSE" ] || [ ! -f "README.md" ] || [ ! -f "pyproject.toml" ]; then
  warn "当前目录似乎不是 bookmind-agent-suite 根目录：缺 LICENSE/README.md/pyproject.toml"
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  warn "未安装 git"
  exit 1
fi

# 2) 初始化
if [ -d ".git" ]; then
  info "已存在 .git，复用"
else
  info "git init"
  git init -q
  git checkout -q -b "$DEFAULT_BRANCH"
fi

git config user.name  "$COMMIT_AUTHOR_NAME"
git config user.email "$COMMIT_AUTHOR_EMAIL"

# 3) 首次 commit
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  info "已有 commit history，跳过首次 commit"
else
  info "添加文件 + 首次 commit"
  git add -A
  git commit -q -m "feat: initial release of BookMind v1.0.0

- 13 specialized agents (BookDirector + 12 workers)
- 10 OpenClaw/Hermes compatible Skills
- Hermes skill bundle: book-reading-suite.yaml
- PDF parsing (PyMuPDF + pypdf + optional OCR)
- 8 export formats (md/html/json/csv/anki/obsidian/mermaid/pdf)
- Typer CLI + Docker + GitHub Actions CI
- 23 pytest tests
- Apache 2.0 License"
fi

# 4) 远程
if git remote get-url origin >/dev/null 2>&1; then
  warn "remote origin 已存在：$(git remote get-url origin)"
  warn "如需更换，请执行：git remote remove origin 后重跑"
else
  info "添加 remote: $REPO_URL"
  git remote add origin "$REPO_URL"
fi

# 5) 推送
info "推送到 $DEFAULT_BRANCH ..."
git push -u origin "$DEFAULT_BRANCH" --follow-tags

# 6) 打 tag
info "打 v1.0.0 tag ..."
git tag -f v1.0.0
git push -f origin v1.0.0 || warn "tag 推送失败（可能已存在）"

# 7) 输出 GitHub 后续动作提示
cat <<EOF

${GREEN}============================================${NC}
${GREEN}  BookMind 已发布到 GitHub ${NC}
${GREEN}============================================${NC}

接下来请在 GitHub 网页上完成以下动作（5 分钟）：

1) 打开仓库页面，确认 LICENSE 显示为 Apache-2.0
2) About 栏右侧 ⚙️ 勾选:
   - Description: "Multi-agent deep book reading system for OpenClaw & Hermes"
   - Website: 你的文档地址（可选）
   - Topics: book, pdf, reading, agent, openclaw, hermes,
            knowledge-management, ai-agent, pdf-parser, summarization
3) Releases → Draft a new release → 选择 v1.0.0 tag → 自动生成
4) Settings → General → 勾选 "Automatically delete head branches"
5) Settings → Pages → 选择 gh-pages 分支（如果你用了 Pages 文档）
6) Settings → Security → 启用 Dependabot alerts

可选：克隆仓库后用 gh CLI 一次性配置：
  gh repo edit --enable-issues --enable-projects --enable-wiki=false

EOF

ok "Done."
