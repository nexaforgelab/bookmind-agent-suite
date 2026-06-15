#!/usr/bin/env bash
# ============================================
# BookMind OpenClaw Installation Script
# 安装 BookMind 到 OpenClaw 环境
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

# Detect OpenClaw installation path
detect_openclaw() {
    local paths=("$HOME/.openclaw" "/opt/openclaw" "/usr/local/openclaw")
    
    for path in "${paths[@]}"; do
        if [ -d "$path" ]; then
            echo "$path"
            return 0
        fi
    done
    
    return 1
}

# Install skill bundle
install_skill_bundle() {
    local openclaw_path="$1"
    local skills_dir="$openclaw_path/skills"
    local bundles_dir="$openclaw_path/bundles"
    
    log_info "Installing BookMind skill bundle..."
    
    mkdir -p "$skills_dir" "$bundles_dir"
    
    # Copy skill bundle definition
    cp "$SCRIPT_DIR/skill-bundles/book-reading-suite.yaml" "$bundles_dir/"
    
    # Copy all skills
    if [ -d "$SCRIPT_DIR/skills" ]; then
        cp -r "$SCRIPT_DIR/skills/"* "$skills_dir/"
        log_info "Skills copied to $skills_dir"
    fi
    
    log_info "Skill bundle installed successfully"
}

# Install Python package
install_python_package() {
    log_info "Installing bookmind Python package..."
    pip install -e "$SCRIPT_DIR"
}

# Main
main() {
    log_info "BookMind OpenClaw Installation"
    log_info "================================"
    
    local openclaw_path=$(detect_openclaw)
    
    if [ -z "$openclaw_path" ]; then
        log_error "Could not find OpenClaw installation"
        log_info "Please install OpenClaw first or specify path manually"
        log_info "Usage: OPENCLAW_PATH=/path/to/openclaw $0"
        exit 1
    fi
    
    log_info "Found OpenClaw at: $openclaw_path"
    
    install_python_package
    install_skill_bundle "$openclaw_path"
    
    log_info ""
    log_info "Installation complete!"
    log_info "You can now use BookMind skills in OpenClaw"
}

main "$@"
