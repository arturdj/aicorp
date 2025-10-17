#!/bin/bash

# AI Corp WebUI API Client - Uninstall Script
# This script removes the aicorp client and cleans up the environment

set -e  # Exit on any error

echo "🗑️  AI Corp WebUI API Client - Uninstall Script"
echo "==============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to ask for user confirmation
ask_confirmation() {
    local prompt="$1"
    local default="${2:-n}"
    
    if [ "$default" = "y" ]; then
        prompt="$prompt [Y/n]: "
    else
        prompt="$prompt [y/N]: "
    fi
    
    read -p "$prompt" response
    response=${response:-$default}
    
    case "$response" in
        [yY][eE][sS]|[yY]) 
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Check if aicorp is installed
print_status "Checking if aicorp is installed..."
if command -v aicorp &> /dev/null; then
    print_success "aicorp command found"
    AICORP_INSTALLED=true
else
    print_warning "aicorp command not found in PATH"
    AICORP_INSTALLED=false
fi

# Check if package is installed via pip
print_status "Checking pip installation..."
if pip3 show aicorp-client &> /dev/null; then
    print_success "aicorp-client package found in pip"
    PIP_INSTALLED=true
else
    print_warning "aicorp-client package not found in pip"
    PIP_INSTALLED=false
fi

# If nothing is installed, exit
if [ "$AICORP_INSTALLED" = false ] && [ "$PIP_INSTALLED" = false ]; then
    print_warning "No aicorp installation found. Nothing to uninstall."
    exit 0
fi

echo ""
print_status "The following will be removed:"
if [ "$PIP_INSTALLED" = true ]; then
    echo "  • aicorp-client Python package"
fi
if [ "$AICORP_INSTALLED" = true ]; then
    echo "  • aicorp command from ~/.local/bin"
fi
echo ""

# Ask for confirmation
if ! ask_confirmation "Do you want to proceed with uninstallation?"; then
    print_status "Uninstallation cancelled by user."
    exit 0
fi

echo ""

# Uninstall the pip package
if [ "$PIP_INSTALLED" = true ]; then
    print_status "Uninstalling aicorp-client package..."
    if pip3 uninstall aicorp-client -y; then
        print_success "Package uninstalled successfully"
    else
        print_error "Failed to uninstall package"
        exit 1
    fi
fi

# Check if command is still available
print_status "Verifying command removal..."
if command -v aicorp &> /dev/null; then
    print_warning "aicorp command still found in PATH"
    print_warning "This might be due to shell caching. Try: hash -r"
else
    print_success "aicorp command removed successfully"
fi

# Ask about configuration cleanup
echo ""
print_status "Configuration cleanup options:"

# Ask about .env file
if [ -f .env ]; then
    echo ""
    if ask_confirmation "Remove .env configuration file? (contains API keys)"; then
        rm .env
        print_success "Removed .env file"
    else
        print_status "Keeping .env file"
    fi
fi

# Ask about log files
if [ -f aicorp.log ]; then
    echo ""
    if ask_confirmation "Remove aicorp.log file?"; then
        rm aicorp.log
        print_success "Removed aicorp.log file"
    else
        print_status "Keeping aicorp.log file"
    fi
fi

# Check for PATH modifications
echo ""
print_status "Checking PATH modifications..."

PATH_MODIFIED=false
SHELL_RC=""

# Check common shell configuration files
if [ -f ~/.bashrc ] && grep -q "\.local/bin" ~/.bashrc; then
    SHELL_RC="~/.bashrc"
    PATH_MODIFIED=true
elif [ -f ~/.zshrc ] && grep -q "\.local/bin" ~/.zshrc; then
    SHELL_RC="~/.zshrc"
    PATH_MODIFIED=true
elif [ -f ~/.profile ] && grep -q "\.local/bin" ~/.profile; then
    SHELL_RC="~/.profile"
    PATH_MODIFIED=true
fi

if [ "$PATH_MODIFIED" = true ]; then
    echo ""
    print_warning "Found PATH modification in $SHELL_RC"
    echo "The following line adds ~/.local/bin to PATH:"
    if [ "$SHELL_RC" = "~/.bashrc" ]; then
        grep "\.local/bin" ~/.bashrc
    elif [ "$SHELL_RC" = "~/.zshrc" ]; then
        grep "\.local/bin" ~/.zshrc
    elif [ "$SHELL_RC" = "~/.profile" ]; then
        grep "\.local/bin" ~/.profile
    fi
    echo ""
    print_warning "This was likely added for aicorp, but ~/.local/bin may be used by other applications."
    print_warning "Please manually review and remove the PATH modification if no longer needed."
    echo ""
    echo "To remove it, edit $SHELL_RC and delete the line containing '~/.local/bin'"
else
    print_success "No PATH modifications found in common shell configuration files"
fi

# Clean up Python cache if in development directory
if [ -d "__pycache__" ]; then
    echo ""
    if ask_confirmation "Remove Python cache files (__pycache__)?"; then
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -name "*.pyc" -delete 2>/dev/null || true
        print_success "Removed Python cache files"
    fi
fi

# Clean up build artifacts if in development directory
if [ -d "build" ] || [ -d "dist" ] || [ -d "*.egg-info" ]; then
    echo ""
    if ask_confirmation "Remove build artifacts (build/, dist/, *.egg-info)?"; then
        rm -rf build/ dist/ *.egg-info/ 2>/dev/null || true
        print_success "Removed build artifacts"
    fi
fi

echo ""
print_success "Uninstallation completed!"
echo ""
echo "Summary:"
echo "• aicorp-client package has been removed"
echo "• aicorp command is no longer available"
if [ "$PATH_MODIFIED" = true ]; then
    echo "• Please manually review PATH modifications in $SHELL_RC"
fi
echo ""
echo "If you want to reinstall later, run: ./scripts/install.sh"
echo ""
