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
