# Changelog

All notable changes to the aicorp-client project.

## [1.2.1] - 2025-10-17

### Added
- Index-based model selection in configuration setup
- Dual input support for model selection (index numbers and full names)
- Input validation for model index ranges

### Changed
- Enhanced model selection logic to detect numeric vs text input
- Improved configuration prompts for model selection
- Added bounds checking for model indices

### Fixed
- Error handling for invalid model index selections

## [1.2.0] - 2025-10-17

### Removed
- `requirements.txt` - Dependencies now managed only via `pyproject.toml`
- `verify_setup.py` - Legacy setup verification script

### Changed
- Python version requirement updated from 3.7+ to 3.8+ in `install.sh`
- Project root detection in `config_manager.py` no longer checks for `setup.py` or `requirements.txt`
- `MANIFEST.in` no longer includes `requirements.txt`
- CHANGELOG references updated to reflect `pyproject.toml`-only approach

### Fixed
- Consistent Python 3.8+ requirement across all project files

## [1.1.2] - 2025-10-17

### Breaking Changes
- `WEBUI_API_KEY` environment variable is now required for all operations
- Configuration validation prevents initialization without API key

### Added
- Strict validation for API key and base URL at startup
- Test cases for missing API key validation
- Error messages for missing API key scenarios

### Changed
- Authorization header is always included in requests
- Configuration setup requires API key input with validation
- `get_available_models()` requires both base URL and API key
- Updated test suite to handle mandatory API key requirement
- Updated `.env.example` with cleaner API key format

### Migration Notes
- Ensure `WEBUI_API_KEY` is configured in environment
- Run `aicorp --config` to add API key to existing configuration
- Update automation scripts to include API key in environment variables

## [1.1.1] - 2025-10-17

### Added
- Comprehensive input validation for all user inputs and API parameters
- Parameter whitelisting for API parameters (max_tokens, temperature, top_p, stream, top_k, frequency_penalty, presence_penalty, stop, seed)
- Range validation for numeric parameters (temperature: 0.0-2.0, max_tokens: 1-32768)
- Message structure validation for chat messages
- Type checking with clear error messages
- Input validation tests and parameter range tests

### Changed
- API keys are properly masked in debug logs
- Graceful error handling with proper logging
- Validated file paths and encoding handling

### Removed
- Hardcoded API key from repository
- 20+ unused ANSI color codes, keeping only 8 used colors
- Unused development dependencies (black, flake8, mypy)
- Unused tool configurations from pyproject.toml
- Temporary log files and cache files

### Fixed
- Package version synchronization across all files

## [1.1.0] - 2025-10-16

### Added
- Environment detection for virtual environments vs system installations
- Interactive PATH configuration for shell setup
- Shell-specific instructions (zsh, bash, etc.)
- Comprehensive uninstall script with optional cleanup
- PATH modification detection and warnings
- urllib3 compatibility checking
- Enhanced error reporting and suggestions

### Changed
- Install script now handles pip upgrades automatically
- Dependency management consolidated to `pyproject.toml` only
- Enhanced install.sh with virtual environment detection and interactive PATH setup
- Updated dist.sh to include uninstall script
- Improved dependency resolution for different Python environments

### Fixed
- urllib3 v2.x compatibility issues on macOS systems (added `urllib3>=1.26.0,<2.0.0` constraint)
- PATH detection for user site-packages bin directory
- Environment handling for both virtual and system Python environments

## [1.0.0] - Previous Release

### Added
- AI Corp WebUI API client implementation
- Command-line interface with model management
- Configuration system with environment variables
- Installation and setup scripts
- Test suite and documentation
- Python packaging structure
