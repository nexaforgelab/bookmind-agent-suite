#!/usr/bin/env bash
# ============================================
# BookMind Hermes Installation Script
# 安装 BookMind 到 Hermes 环境
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

# Detect Hermes installation path
detect_hermes() {
    local paths=("$HOME/.hermes" "/opt/hermes" "/usr/local/hermes")
    
    for path in "${paths[@]}"; do
        if [ -d "$path" ]; then
            echo "$path"
            return 0
        fi
    done
    
    return 1
}

# Install skill definitions
install_skills() {
    local hermes_path="$1"
    local skills_dir="$hermes_path/skills"
    
    log_info "Installing BookMind skills to Hermes..."
    
    mkdir -p "$skills_dir"
    
    # Copy skills with hermes-compatible structure
    if [ -d "$SCRIPT_DIR/skills" ]; then
        for skill_dir in "$SCRIPT_DIR/skills"/*/; do
            skill_name=$(basename "$skill_dir")
            target_dir="$skills_dir/$skill_name"
            
            mkdir -p "$target_dir"
            cp "$skill_dir/SKILL.md" "$target_dir/" 2>/dev/null || true
            cp -r "$skill_dir/scripts" "$target_dir/" 2>/dev/null || true
            
            log_info "  - Installed skill: $skill_name"
        done
    fi
    
    log_info "Skills installed to $skills_dir"
}

# Install Python package
install_python_package() {
    log_info "Installing bookmind Python package..."
    pip install -e "$SCRIPT_DIR"
}

# Configure Hermes
configure_hermes() {
    local hermes_path="$1"
    local config_file="$hermes_path/config/bookmind.json"
    
    log_info "Configuring Hermes integration..."
    
    mkdir -p "$(dirname "$config_file")"
    
    cat > "$config_file" << 'EOF'
{
    "enabled": true,
    "skill_path": "${HERMES_PATH}/skills",
    "default_timeout": 300,
    "max_workers": 4
}
EOF
    
    log_info "Configuration written to $config_file"
}

# Main
main() {
    log_info "BookMind Hermes Installation"
    log_info "================================"
    
    local hermes_path=$(detect_hermes)
    
    if [ -z "$hermes_path" ]; then
        log_error "Could not find Hermes installation"
        log_info "Please install Hermes first or specify path manually"
        log_info "Usage: HERMES_PATH=/path/to/hermes $0"
        exit 1
    fi
    
    log_info "Found Hermes at: $hermes_path"
    
    install_python_package
    install_skills "$hermes_path"
    configure_hermes "$hermes_path"
    
    log_info ""
    log_info "Installation complete!"
    log_info "You can now use BookMind skills in Hermes"
    log_info "Try: hermes run book-deep-reading /path/to/book.pdf"
}

main "$@"
