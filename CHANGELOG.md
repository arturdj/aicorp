# Changelog

All notable changes to the AI Corp WebUI API Client project are documented in this file.

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

### 🔒 Breaking Changes

#### API Key Requirements
- **Mandatory API Key**: `WEBUI_API_KEY` environment variable is now required for all operations
- **Configuration Validation**: Added strict validation that prevents initialization without API key
- **Interactive Setup**: Configuration setup now requires API key input and validates it's provided
- **Error Handling**: Clear error messages when API key is missing: "WEBUI_API_KEY environment variable is required"

### 🛠️ Technical Improvements

#### Configuration System
- **Enhanced Validation**: Both `WEBUI_BASE_URL` and `WEBUI_API_KEY` are now mandatory at startup
- **Simplified Headers**: Authorization header is always included since API key is guaranteed to exist
- **Config Manager Updates**: Removed "optional" language from API key setup, added validation loop
- **Model Fetching**: `get_available_models()` now requires both base URL and API key before attempting API calls

#### Testing & Quality
- **Updated Test Suite**: All tests now properly handle mandatory API key requirement
- **New Test Cases**: Added specific tests for missing API key and base URL validation
- **Error Scenario Coverage**: Comprehensive testing of configuration validation failures
- **Backward Compatibility**: Removed tests that expected API key to be optional

#### Documentation Updates
- **Environment Examples**: Updated `.env.example` with cleaner API key format
- **Setup Instructions**: Configuration examples now emphasize API key requirement
- **Error Documentation**: Clear guidance on resolving missing API key errors

### 🚨 Migration Notes

**For existing users upgrading to v1.1.2:**

1. **Ensure API Key is Set**: Verify your `.env` file or environment has `WEBUI_API_KEY` configured
2. **Update Configuration**: Run `aicorp --setup` if you need to add an API key to existing configuration
3. **Check Scripts**: Any automation scripts must include API key in environment variables

**Breaking Change Impact:**
- Applications that previously worked without API key will now fail with clear error message
- This change improves security by ensuring all API calls are properly authenticated
- No functional changes for users who already had API key configured

## [1.1.1] - 2025-10-17

### 🔒 Security Enhancements

#### Input Validation & Security
- **Comprehensive Input Validation**: Added validation for all user inputs and API parameters
- **Parameter Whitelisting**: Only allows validated API parameters (max_tokens, temperature, top_p, stream, top_k, frequency_penalty, presence_penalty, stop, seed)
- **Range Validation**: Numeric parameters validated against safe ranges (e.g., temperature: 0.0-2.0, max_tokens: 1-32768)
- **Message Structure Validation**: Chat messages validated for proper structure and non-empty content
- **Type Checking**: Strict type validation for all parameters with clear error messages

#### Security Audit & Cleanup
- **Removed Hardcoded Secrets**: Eliminated hardcoded API key from repository
- **Safe Error Handling**: Graceful degradation with proper logging instead of exposing internal errors
- **Secret Masking**: API keys properly masked in debug logs
- **Secure File Operations**: Validated file paths and proper encoding handling

### 🧹 Code Cleanup & Optimization

#### Deprecated Code Removal
- **Unused Color Constants**: Removed 20+ unused ANSI color codes, keeping only 8 used colors
- **Version Synchronization**: Updated package version to 1.1.0 across all files
- **Dependency Cleanup**: Removed unused development dependencies (black, flake8, mypy)
- **Configuration Cleanup**: Removed unused tool configurations from pyproject.toml
- **File Cleanup**: Removed temporary log files and cache files

#### Performance Improvements
- **Reduced Package Size**: Smaller codebase with optimized dependencies
- **Faster Installation**: Fewer optional dependencies to install
- **Better Maintainability**: Cleaner code structure with consistent formatting

### 🧪 Enhanced Testing

#### Security Testing
- **Input Validation Tests**: Comprehensive test coverage for all validation scenarios
- **Parameter Range Tests**: Tests for out-of-range values and invalid types
- **Error Handling Tests**: Validation of proper error responses and logging

## [1.1.0] - 2025-10-16

### 🚀 Major Enhancements

#### Installation & Setup
- **Smart Environment Detection**: Automatically detects virtual environments vs system installations
- **Interactive PATH Configuration**: Offers to automatically add aicorp to shell configuration
- **Shell-Aware Instructions**: Provides tailored setup commands for zsh, bash, and other shells
- **Pip Version Management**: Automatically upgrades pip for modern Python packaging support
- **Enhanced Install Script**: Comprehensive installation with user-friendly guidance

#### System Management
- **Comprehensive Uninstall Script**: Complete removal with optional cleanup of configs and cache
- **PATH Analysis**: Detects and warns about shell configuration modifications
- **Dependency Management**: Proper version constraints for stable operation
- **Cross-Platform Support**: Improved compatibility with macOS system Python and virtual environments

#### Bug Fixes
- **LibreSSL Compatibility**: Fixed urllib3 v2.x compatibility issues on macOS systems
- **PATH Detection**: Accurate detection of user site-packages bin directory
- **Environment Handling**: Proper handling of both virtual and system Python environments

### 🛠️ Technical Improvements

#### Dependencies
- Added `urllib3>=1.26.0,<2.0.0` constraint for LibreSSL compatibility
- Consolidated dependency management to use only `pyproject.toml`
- Improved dependency resolution for different Python environments

#### Scripts & Tools
- **Enhanced install.sh**: 
  - Virtual environment detection
  - Interactive PATH setup with auto-configuration option
  - Shell-specific instructions (zsh, bash, etc.)
  - Pip upgrade handling
  - Comprehensive error handling and user feedback

- **New uninstall.sh**:
  - Interactive uninstall with user confirmation
  - Optional cleanup of configuration files and logs
  - PATH modification detection and warnings
  - Python cache and build artifact cleanup
  - Colored output for better user experience

- **Updated dist.sh**: 
  - Includes uninstall script in distribution
  - Updated distribution documentation
  - Enhanced feature descriptions

- **Enhanced verify_setup.py**:
  - urllib3 compatibility checking
  - More comprehensive dependency verification
  - Better error reporting and suggestions

#### Documentation
- **Updated README.md**: 
  - New "Key Features" section highlighting installation improvements
  - Enhanced installation instructions with feature descriptions
  - Updated uninstallation section with comprehensive options

- **Enhanced INSTALL.md**: 
  - Detailed uninstallation procedures
  - Multiple uninstall options (comprehensive, quick, manual)
  - Makefile integration instructions

- **Updated Makefile**: 
  - Comprehensive uninstall target using new script
  - Enhanced help text with all available commands
  - Additional phony targets for better organization

### 🎯 User Experience Improvements

#### Installation Experience
- **One-Click Setup**: `./scripts/install.sh` handles everything automatically
- **Smart Guidance**: Context-aware instructions based on user's environment
- **Interactive Options**: Optional automatic configuration with user consent
- **Clear Feedback**: Colored output and progress indicators throughout

#### Uninstallation Experience
- **Safe Removal**: Interactive confirmation for each cleanup step
- **Selective Cleanup**: Users can choose what to remove
- **PATH Guidance**: Warns about shell configuration modifications
- **Complete or Partial**: Options for comprehensive or package-only removal

#### Error Handling
- **Better Diagnostics**: More informative error messages and suggestions
- **Environment Awareness**: Different handling for virtual vs system environments
- **Compatibility Checks**: Proactive detection of potential issues

### 📦 Distribution Improvements

#### Package Management
- **Modern Packaging**: Full pyproject.toml compliance with proper dependency management
- **Distribution Ready**: Enhanced dist.sh script for easy package creation
- **Installation Verification**: Comprehensive setup verification with multiple checks

#### Documentation
- **Complete Instructions**: Step-by-step guides for all installation methods
- **Troubleshooting**: Common issues and solutions documented
- **Feature Highlights**: Clear documentation of all capabilities

## [1.0.0] - Previous Release

### Initial Features
- AI Corp WebUI API client implementation
- Command-line interface with model management
- Configuration system with environment variables
- Basic installation and setup scripts
- Test suite and documentation
- Modern Python packaging structure

---

## Installation

To get the latest version with all enhancements:

```bash
git clone <repository-url>
cd aicorp-client
./scripts/install.sh
```

## Uninstallation

To remove the client completely:

```bash
./scripts/uninstall.sh
```

For more details, see [INSTALL.md](INSTALL.md) and [README.md](README.md).
