#!/bin/bash

# AI Corp WebUI API Client - Distribution Preparation Script
# This script prepares the project for distribution to end users

set -e

echo "📦 Preparing AI Corp WebUI API Client for distribution..."
echo

# Clean any existing build artifacts
echo "🧹 Cleaning build artifacts..."
rm -rf build/ dist/ *.egg-info/
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/install.sh
chmod +x scripts/uninstall.sh
chmod +x verify_setup.py
chmod +x scripts/dist.sh

# Verify project structure
echo "🔍 Verifying project structure..."
required_files=(
    "pyproject.toml"
    "README.md"
    "INSTALL.md"
    "scripts/install.sh"
    "scripts/uninstall.sh"
    "verify_setup.py"
    ".env.example"
    "config/system_prompt.txt"
    "src/aicorp/__init__.py"
    "src/aicorp/cli.py"
    "src/aicorp/api_client.py"
    "src/aicorp/config.py"
    "src/aicorp/logger.py"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Missing required files:"
    printf '   %s\n' "${missing_files[@]}"
    exit 1
fi

echo "✅ All required files present"

# Test installation in a temporary environment (optional)
if command -v python3 &> /dev/null; then
    echo "🧪 Testing installation..."
    
    # Create a temporary directory for testing
    temp_dir=$(mktemp -d)
    cp -r . "$temp_dir/"
    
    # Test installation
    cd "$temp_dir"
    if python3 -m pip install -e . --user --quiet; then
        echo "✅ Installation test passed"
        
        # Test basic functionality
        if python3 -c "from aicorp import AiCorpClient, Config; print('Import test passed')"; then
            echo "✅ Import test passed"
        else
            echo "❌ Import test failed"
        fi
    else
        echo "❌ Installation test failed"
    fi
    
    # Cleanup
    cd - > /dev/null
    rm -rf "$temp_dir"
fi

# Create distribution archive
echo "📦 Creating distribution archive..."
project_name="aicorp-client"
archive_name="${project_name}-$(date +%Y%m%d-%H%M%S).tar.gz"

# Create archive excluding unnecessary files
tar -czf "$archive_name" \
    --exclude='.git*' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='build' \
    --exclude='dist' \
    --exclude='*.egg-info' \
    --exclude='.env' \
    --exclude='*.log' \
    --exclude='.DS_Store' \
    --exclude='*.tar.gz' \
    .

echo "✅ Created distribution archive: $archive_name"

# Generate installation instructions
cat > DISTRIBUTION_README.txt << EOF
AI Corp WebUI API Client - Distribution Package
===============================================

This package contains the AI Corp WebUI API client for macOS.

QUICK INSTALLATION:
1. Extract this archive
2. cd aicorp-client/
3. ./scripts/install.sh
4. Follow the PATH setup instructions (automatic option available)

MANUAL INSTALLATION:
1. Extract this archive
2. cd aicorp-client/
3. pip3 install -e . --user
4. Add ~/.local/bin or user site-packages bin to PATH
5. cp .env.example .env
6. Edit .env with your API credentials

UNINSTALLATION:
Run: ./scripts/uninstall.sh (comprehensive cleanup)
Or: pip3 uninstall aicorp-client (package only)

VERIFICATION:
Run: python3 verify_setup.py

USAGE:
aicorp --help
aicorp --list-models
aicorp "Hello, world!"

FEATURES:
- Virtual environment detection
- Automatic PATH configuration
- urllib3 LibreSSL compatibility
- Interactive installation assistance
- Comprehensive uninstall option

For detailed instructions, see README.md and INSTALL.md

Support: Check the project repository for issues and documentation.
EOF

echo "✅ Created DISTRIBUTION_README.txt"

# Show distribution contents
echo
echo "📋 Distribution contents:"
echo "   Archive: $archive_name"
echo "   Size: $(du -h "$archive_name" | cut -f1)"
echo "   Instructions: DISTRIBUTION_README.txt"
echo

echo "🎉 Distribution package ready!"
echo
echo "📤 To share with users:"
echo "   1. Send them the $archive_name file"
echo "   2. Include DISTRIBUTION_README.txt for instructions"
echo "   3. They can run ./scripts/install.sh for automatic setup"
