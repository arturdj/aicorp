#!/bin/bash

# AI Corp WebUI API Client - Installation Script
# This script installs the aicorp client and sets up the environment

set -e  # Exit on any error

echo "🚀 AI Corp WebUI API Client - Installation Script"
echo "=================================================="

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

# Check Python version
print_status "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION found"
    
    # Check if Python version is 3.7 or higher
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 7 ]; then
        print_success "Python version is compatible (3.7+)"
    else
        print_error "Python 3.7 or higher is required. Found: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check pip
print_status "Checking pip..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version | awk '{print $2}')
    print_success "pip3 found (version $PIP_VERSION)"
    
    # Check if pip version supports pyproject.toml editable installs (requires pip >= 21.3)
    PIP_MAJOR=$(echo $PIP_VERSION | cut -d. -f1)
    PIP_MINOR=$(echo $PIP_VERSION | cut -d. -f2)
    
    if [ "$PIP_MAJOR" -lt 21 ] || ([ "$PIP_MAJOR" -eq 21 ] && [ "$PIP_MINOR" -lt 3 ]); then
        print_warning "pip version $PIP_VERSION is too old for pyproject.toml editable installs"
        print_status "Upgrading pip..."
        
        # Detect if we're in a virtual environment for pip upgrade
        if [[ -n "$VIRTUAL_ENV" ]] || [[ -n "$CONDA_DEFAULT_ENV" ]] || python3 -c "import sys; exit(0 if sys.prefix != sys.base_prefix else 1)" 2>/dev/null; then
            PIP_UPGRADE_CMD="python3 -m pip install --upgrade pip"
        else
            PIP_UPGRADE_CMD="python3 -m pip install --upgrade pip --user"
        fi
        
        if $PIP_UPGRADE_CMD; then
            print_success "pip upgraded successfully"
        else
            print_warning "Failed to upgrade pip, but continuing with installation"
        fi
    fi
else
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

# Detect virtual environment
print_status "Detecting environment..."
if [[ -n "$VIRTUAL_ENV" ]] || [[ -n "$CONDA_DEFAULT_ENV" ]] || python3 -c "import sys; exit(0 if sys.prefix != sys.base_prefix else 1)" 2>/dev/null; then
    print_success "Virtual environment detected"
    VENV_MODE=true
    INSTALL_CMD="pip3 install -e ."
else
    print_success "System environment detected"
    VENV_MODE=false
    INSTALL_CMD="pip3 install -e . --user"
fi

# Install the package in development mode
print_status "Installing aicorp client in development mode..."
print_status "Using command: $INSTALL_CMD"
if $INSTALL_CMD; then
    print_success "Package installed successfully"
else
    print_error "Failed to install package"
    exit 1
fi

# Check PATH configuration based on environment
print_status "Checking PATH configuration..."
if [ "$VENV_MODE" = true ]; then
    if [[ -n "$VIRTUAL_ENV" ]]; then
        VENV_BIN="$VIRTUAL_ENV/bin"
        if [[ ":$PATH:" == *":$VENV_BIN:"* ]]; then
            print_success "Virtual environment bin directory is in PATH"
        else
            print_warning "Virtual environment bin directory not in PATH"
            print_warning "This is unusual - virtual environments should automatically add their bin to PATH"
        fi
    else
        print_success "In virtual environment - PATH should be automatically configured"
    fi
else
    # Detect the actual user site-packages bin directory
    USER_BIN_DIR=$(python3 -m site --user-base)/bin
    
    if [[ ":$PATH:" == *":$USER_BIN_DIR:"* ]]; then
        print_success "$USER_BIN_DIR is already in PATH"
    else
        print_warning "$USER_BIN_DIR is not in PATH"
        echo ""
        echo "To add it to your PATH, run one of these commands:"
        echo ""
        echo "For bash:"
        echo "  echo 'export PATH=\"$USER_BIN_DIR:\$PATH\"' >> ~/.bashrc"
        echo "  source ~/.bashrc"
        echo ""
        echo "For zsh:"
        echo "  echo 'export PATH=\"$USER_BIN_DIR:\$PATH\"' >> ~/.zshrc"
        echo "  source ~/.zshrc"
        echo ""
        echo "Or add the generic user bin directory:"
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
        echo ""
    fi
fi

# Set up .env file if it doesn't exist
print_status "Setting up environment configuration..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        print_success "Created .env file from .env.example"
        print_warning "Please edit .env file with your API credentials"
    else
        print_error ".env.example file not found"
        exit 1
    fi
else
    print_success ".env file already exists"
fi

# Verify installation
print_status "Verifying installation..."
if command -v aicorp &> /dev/null; then
    print_success "aicorp command is available"
    
    # Test basic functionality
    print_status "Testing basic functionality..."
    if aicorp --help > /dev/null 2>&1; then
        print_success "aicorp command works correctly"
    else
        print_warning "aicorp command found but may have issues"
    fi
else
    print_warning "aicorp command not found in PATH"
    if [ "$VENV_MODE" = true ]; then
        print_warning "Make sure your virtual environment is activated"
        print_warning "Try: source .venv/bin/activate (or your venv path)"
    else
        USER_BIN_DIR=$(python3 -m site --user-base)/bin
        print_warning "You may need to add $USER_BIN_DIR to your PATH"
        print_warning "Quick fix: export PATH=\"$USER_BIN_DIR:\$PATH\""
        print_warning "Or restart your terminal after updating your shell config"
    fi
fi

echo ""
print_success "Installation completed!"
echo ""

# Check if PATH needs to be updated and provide clear instructions
if [ "$VENV_MODE" = false ]; then
    USER_BIN_DIR=$(python3 -m site --user-base)/bin
    if [[ ":$PATH:" != *":$USER_BIN_DIR:"* ]]; then
        echo "🔧 IMPORTANT: Add aicorp to your PATH permanently"
        echo "=============================================="
        echo ""
        echo "The aicorp command was installed to: $USER_BIN_DIR"
        echo ""
        echo "To use aicorp from anywhere, add this directory to your PATH:"
        echo ""
        
        # Detect current shell
        CURRENT_SHELL=$(basename "$SHELL")
        if [ "$CURRENT_SHELL" = "zsh" ]; then
            echo "📝 For zsh (your current shell):"
            echo "   echo 'export PATH=\"$USER_BIN_DIR:\$PATH\"' >> ~/.zshrc"
            echo "   source ~/.zshrc"
        elif [ "$CURRENT_SHELL" = "bash" ]; then
            echo "📝 For bash (your current shell):"
            echo "   echo 'export PATH=\"$USER_BIN_DIR:\$PATH\"' >> ~/.bashrc"
            echo "   source ~/.bashrc"
        else
            echo "📝 For your shell ($CURRENT_SHELL):"
            echo "   echo 'export PATH=\"$USER_BIN_DIR:\$PATH\"' >> ~/.${CURRENT_SHELL}rc"
            echo "   source ~/.${CURRENT_SHELL}rc"
        fi
        
        echo ""
        echo "💡 Quick test (temporary for this session):"
        echo "   export PATH=\"$USER_BIN_DIR:\$PATH\""
        echo "   aicorp --help"
        echo ""
        
        # Ask if user wants to automatically add to shell config
        echo "🤖 Would you like me to add this to your shell configuration automatically? [y/N]"
        read -r AUTO_ADD_PATH
        
        if [[ "$AUTO_ADD_PATH" =~ ^[Yy]$ ]]; then
            SHELL_CONFIG=""
            if [ "$CURRENT_SHELL" = "zsh" ]; then
                SHELL_CONFIG="$HOME/.zshrc"
            elif [ "$CURRENT_SHELL" = "bash" ]; then
                SHELL_CONFIG="$HOME/.bashrc"
            else
                SHELL_CONFIG="$HOME/.${CURRENT_SHELL}rc"
            fi
            
            # Check if PATH export already exists
            if [ -f "$SHELL_CONFIG" ] && grep -q "export PATH.*$USER_BIN_DIR" "$SHELL_CONFIG"; then
                print_warning "PATH export already exists in $SHELL_CONFIG"
            else
                echo "export PATH=\"$USER_BIN_DIR:\$PATH\"" >> "$SHELL_CONFIG"
                print_success "Added PATH export to $SHELL_CONFIG"
                print_status "Run 'source $SHELL_CONFIG' or restart your terminal to apply changes"
            fi
        else
            print_status "Skipped automatic PATH configuration"
        fi
        
        echo ""
        echo "=============================================="
        echo ""
    fi
fi

echo "Next steps:"
echo "1. Add aicorp to your PATH (see instructions above if needed)"
echo "2. Edit the .env file with your API credentials"
echo "3. Test the installation with: aicorp --help"
echo "4. List available models with: aicorp --list-models"
echo "5. Send a test prompt with: aicorp \"Hello, world!\""
echo ""
echo "For more information, see README.md"
