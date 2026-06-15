#!/usr/bin/env bash
# ============================================
# BookMind Uninstallation Script
# 卸载 BookMind
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Uninstall Python package
uninstall_python_package() {
    log_info "Uninstalling bookmind Python package..."
    pip uninstall -y bookmind 2>/dev/null || true
    log_info "Python package uninstalled"
}

# Remove from OpenClaw
remove_from_openclaw() {
    local openclaw_path="$1"
    local skills_dir="$openclaw_path/skills"
    local bundles_dir="$openclaw_path/bundles"
    
    log_info "Removing from OpenClaw ($openclaw_path)..."
    
    # Remove skill bundle
    rm -f "$bundles_dir/book-reading-suite.yaml" 2>/dev/null || true
    
    # Remove skills (keep directory, only remove bookmind skills)
    if [ -d "$skills_dir" ]; then
        rm -rf "$skills_dir/book-"* 2>/dev/null || true
    fi
    
    log_info "OpenClaw integration removed"
}

# Remove from Hermes
remove_from_hermes() {
    local hermes_path="$1"
    local skills_dir="$hermes_path/skills"
    
    log_info "Removing from Hermes ($hermes_path)..."
    
    if [ -d "$skills_dir" ]; then
        rm -rf "$skills_dir/book-"* 2>/dev/null || true
    fi
    
    # Remove config
    rm -f "$hermes_path/config/bookmind.json" 2>/dev/null || true
    
    log_info "Hermes integration removed"
}

# Main
main() {
    log_info "BookMind Uninstallation"
    log_info "================================"
    
    log_warn "This will remove BookMind from your system"
    read -p "Continue? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Uninstallation cancelled"
        exit 0
    fi
    
    uninstall_python_package
    
    # Try OpenClaw
    if openclaw_path=$(python3 -c "import os; paths=['$HOME/.openclaw','/opt/openclaw','/usr/local/openclaw']; print([p for p in paths if os.path.isdir(p)][0] if any([os.path.isdir(p) for p in paths]) else '')" 2>/dev/null) && [ -n "$openclaw_path" ]; then
        remove_from_openclaw "$openclaw_path"
    fi
    
    # Try Hermes
    if hermes_path=$(python3 -c "import os; paths=['$HOME/.hermes','/opt/hermes','/usr/local/hermes']; print([p for p in paths if os.path.isdir(p)][0] if any([os.path.isdir(p) for p in paths]) else '')" 2>/dev/null) && [ -n "$hermes_path" ]; then
        remove_from_hermes "$hermes_path"
    fi
    
    log_info ""
    log_info "Uninstallation complete!"
    log_info "Note: User data directories were preserved for safety"
    log_info "You can manually remove: ~/.bookmind ~/BookMind"
}

main "$@"
