#!/usr/bin/env bash
# ============================================
# BookMind Publish Script
# 发布脚本：构建、测试、发布到 PyPI
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check for required tools
check_tools() {
    log_info "Checking required tools..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "python3 not found"
        exit 1
    fi
    
    if ! command -v pip &> /dev/null; then
        log_error "pip not found"
        exit 1
    fi
}

# Build package
build_package() {
    log_info "Building package..."
    
    pip install --upgrade build twine
    python3 -m build
    
    log_info "Package built successfully"
}

# Run tests
run_tests() {
    log_info "Running tests..."
    pip install -e ".[dev]"
    pytest tests/ -v --cov=bookmind
}

# Upload to PyPI (TestPyPI by default)
upload_package() {
    local repo="${1:-testpypi}"
    
    if [ "$repo" = "pypi" ]; then
        log_warn "Uploading to PRODUCTION PyPI"
        python3 -m twine upload dist/*
    else
        log_info "Uploading to TestPyPI"
        python3 -m twine upload --repository testpypi dist/*
    fi
}

# Clean build artifacts
clean_build() {
    log_info "Cleaning build artifacts..."
    rm -rf dist/ build/ *.egg-info .eggs/
}

# Main
main() {
    check_tools
    
    case "${1:-test}" in
        build)
            build_package
            ;;
        test)
            run_tests
            ;;
        upload-test)
            build_package
            upload_package testpypi
            ;;
        upload-prod)
            build_package
            upload_package pypi
            ;;
        clean)
            clean_build
            ;;
        *)
            echo "Usage: $0 {build|test|upload-test|upload-prod|clean}"
            exit 1
            ;;
    esac
    
    log_info "Done!"
}

main "$@"
