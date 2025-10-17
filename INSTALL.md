# AI Corp WebUI API Client - Installation Guide

This guide provides detailed installation instructions for macOS users to get the `aicorp` command-line tool working in their terminal.

## 🍎 macOS Installation

### Prerequisites

- **macOS 10.14+** (Mojave or later)
- **Python 3.8+** - Check with: `python3 --version`
- **pip** - Usually comes with Python

### Quick Installation (Recommended)

1. **Download the project:**
   ```bash
   git clone <your-repository-url>
   cd aicorp-client
   ```

2. **Run the automated installer:**
   ```bash
   ./install.sh
   ```

3. **Test the installation:**
   ```bash
   aicorp --help
   ```

### Manual Installation

If you prefer to install manually or the script doesn't work:

1. **Install the package:**
   ```bash
   pip3 install -e . --user
   ```

2. **Add to PATH (if needed):**
   
   The `aicorp` command gets installed to `~/.local/bin`. If it's not in your PATH:
   
   ```bash
   # For zsh (default on macOS Catalina+)
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   
   # For bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_profile
   source ~/.bash_profile
   ```

3. **Create configuration file:**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your API settings
   ```

## Configuration

### Environment Variables

Edit the `.env` file with your API credentials:

```bash
# AI Corp WebUI API configuration
WEBUI_BASE_URL=https://ai.corp.azion.com
WEBUI_API_KEY=your_api_key_here

# Default model to use when none is specified
DEFAULT_MODEL=Azion Copilot

# System prompt file path (relative to project root or absolute path)
SYSTEM_PROMPT_FILE=config/system_prompt.txt
```

### API Key Setup

1. Get your API key from your AI Corp dashboard
2. Replace `your_api_key_here` in the `.env` file
3. Save the file

## Verification

Test that everything works:

```bash
# Check if command is available
which aicorp

# Test basic functionality
aicorp --list-models

# Send a test prompt
aicorp "Hello, world!"
```

## Troubleshooting

### Command Not Found

If you get `command not found: aicorp`:

1. **Check if it's installed:**
   ```bash
   ls ~/.local/bin/aicorp
   ```

2. **Add to PATH manually:**
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

3. **Make it permanent:**
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

### Permission Denied

If you get permission errors:

```bash
# Make sure the script is executable
chmod +x ~/.local/bin/aicorp

# Or reinstall with proper permissions
pip3 install -e . --user --force-reinstall
```

### Python Version Issues

If you have multiple Python versions:

```bash
# Use specific Python version
python3.9 -m pip install -e . --user

# Or use pyenv if you have it
pyenv local 3.9.0
pip install -e .
```

### API Connection Issues

If you can't connect to the API:

1. **Check your `.env` file:**
   ```bash
   cat .env
   ```

2. **Test the API URL:**
   ```bash
   curl -I https://ai.corp.azion.com
   ```

3. **Verify API key format:**
   - Make sure there are no extra spaces
   - Check if the key is valid in your dashboard

## Uninstallation

To completely remove the `aicorp` client and clean up your system:

### Comprehensive Uninstall (Recommended)

```bash
# Run the automated uninstall script
./scripts/uninstall.sh
```

The uninstall script will:
- Remove the `aicorp-client` Python package
- Clean up the `aicorp` command from your system
- Optionally remove configuration files (`.env`, log files)
- Detect and warn about PATH modifications
- Clean up Python cache and build artifacts

### Quick Uninstall

If you only want to remove the package:

```bash
pip3 uninstall aicorp-client
```

### Manual Cleanup

If you need to manually clean up:

```bash
# Remove the package
pip3 uninstall aicorp-client -y

# Remove configuration (optional)
rm .env aicorp.log

# Clean Python cache
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# Remove build artifacts
rm -rf build/ dist/ *.egg-info/
```

### Using Makefile

```bash
make uninstall
```

## Development Setup

For developers who want to modify the code:

```bash
# Clone and install in development mode
git clone <repository-url>
cd aicorp-client

# Install with development dependencies
pip3 install -e ".[dev]"

# Run tests
pytest

# Run linting
black src/
flake8 src/
```

## System Integration

### Shell Completion (Optional)

You can add shell completion for better UX:

```bash
# Add to ~/.zshrc
eval "$(_AICORP_COMPLETE=zsh_source aicorp)"

# Or for bash (add to ~/.bashrc)
eval "$(_AICORP_COMPLETE=bash_source aicorp)"
```

### Desktop Integration (Optional)

Create a desktop shortcut:

```bash
# Create application bundle (advanced users)
mkdir -p ~/Applications/AICorp.app/Contents/MacOS
echo '#!/bin/bash\nopen -a Terminal.app ~/.local/bin/aicorp' > ~/Applications/AICorp.app/Contents/MacOS/AICorp
chmod +x ~/Applications/AICorp.app/Contents/MacOS/AICorp
```

## Support

If you encounter issues:

1. Check this troubleshooting guide
2. Verify your Python and pip versions
3. Make sure your API credentials are correct
4. Check the project's issue tracker
5. Contact support with your error messages and system info

### System Information

When reporting issues, include:

```bash
# System info
uname -a
python3 --version
pip3 --version
which aicorp
echo $PATH
```
