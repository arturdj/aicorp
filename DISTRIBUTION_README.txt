aicorp-client Distribution Package v1.2.1
==========================================

Python client library for AI Corp WebUI API.

INSTALLATION:
1. Extract archive
2. cd aicorp-client/
3. ./scripts/install.sh

MANUAL INSTALLATION:
1. Extract archive
2. cd aicorp-client/
3. pip install -e .
4. Configure environment variables

CONFIGURATION:
Run: aicorp --config
Or manually create ~/.azion/.aicorp.env with:
- WEBUI_BASE_URL
- WEBUI_API_KEY
- DEFAULT_MODEL

USAGE:
aicorp --help
aicorp --list-models
aicorp "Hello, world!"

UNINSTALLATION:
./scripts/uninstall.sh

REQUIREMENTS:
- Python 3.8+
- pip

For complete documentation, see README.md
