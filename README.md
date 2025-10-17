# AI Corp WebUI API Client

A modern, well-structured Python client for interacting with AI Corp's WebUI API service for model management and text generation.

## Project Structure

```
aicorp-client/
├── src/aicorp/               # Source code
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Command-line interface
│   ├── api_client.py         # API client implementation
│   ├── config.py             # Configuration management
│   └── logger.py             # Logging utilities
├── config/                   # Configuration files
│   └── system_prompt.txt     # AI system prompt template
├── scripts/                  # Build and installation scripts
│   ├── install.sh            # Installation script
│   ├── uninstall.sh          # Uninstall script
│   └── dist.sh               # Distribution preparation
├── tests/                    # Test suite
│   ├── test_api_client.py    # API client tests
│   └── test_config.py        # Configuration tests
├── docs/                     # Documentation
├── examples/                 # Usage examples
│   └── basic_usage.py        # Basic usage demonstration
├── .env.example              # Environment template
├── pyproject.toml            # Project metadata
├── INSTALL.md                # Installation instructions
└── README.md                 # This file
```

## Modules

### `config.py`
- Handles environment variable loading
- Manages API configuration for AI Corp WebUI service
- Provides headers and endpoint configuration

### `api_client.py`
- Contains the unified `AiCorpClient` class
- Handles HTTP requests to the AI Corp WebUI API
- Supports model listing, text generation, and chat conversations
- Includes comprehensive error handling and logging

### `webui_client.py` (Deprecated)
- Legacy WebUI client - functionality moved to `api_client.py`
- Kept for backward compatibility

### `models.py`
- Parses different API response formats
- Extracts model names from various response structures
- Handles list and dictionary response formats

### `logger.py`
- Configures centralized logging
- Outputs to both file (`aicorp.log`) and console
- Provides structured logging format

### `aicorp.py`
- Main script with command-line interface
- Provides unified interface to AI Corp WebUI API
- Commands for model listing and prompt sending

### `webui_example.py`
- Comprehensive examples of AI Corp WebUI API usage
- Demonstrates simple prompts, chat conversations, and model listing
- Educational resource for AI Corp WebUI integration

## Installation

### 🍎 macOS Quick Install (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd aicorp-client
   ```

2. **Run the installation script:**
   ```bash
   ./scripts/install.sh
   ```
   
   This script will:
   - ✅ Check Python 3.8+ requirements and upgrade pip if needed
   - 🔍 Detect virtual environment vs system installation
   - 📦 Install the `aicorp` command with proper dependencies
   - 🛠️ Fix urllib3 LibreSSL compatibility issues
   - 📝 Create configuration file from template
   - 🎯 Provide shell-specific PATH setup instructions
   - 🤖 Optionally auto-configure your shell PATH

3. **Configure your API settings:**
   ```bash
   # Interactive configuration (recommended)
   aicorp --config
   
   # Or manually edit the .env file
   nano .env
   ```

### Alternative Installation Methods

#### Option 1: Manual pip Installation
```bash
# Install directly with pip
pip install -e . --user

# Add to PATH if needed (add to ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"
```

#### Option 2: Development Installation
```bash
# For developers who want to modify the code
git clone <repository-url>
cd aicorp-client
pip install -e .
```

#### Option 3: From PyPI (when published)
```bash
pip install aicorp-client
```

## Uninstallation

To completely remove the AI Corp client:

```bash
# Comprehensive uninstall (recommended)
./scripts/uninstall.sh
```

The uninstall script will:
- Remove the `aicorp-client` package
- Clean up the `aicorp` command
- Optionally remove configuration and log files
- Clean up Python cache and build artifacts

**Quick uninstall:**
```bash
pip3 uninstall aicorp-client
```

**Using Makefile:**
```bash
make uninstall
```

## Configuration

### Interactive Configuration (Recommended)

Use the interactive configuration command to easily set up your API credentials:

```bash
aicorp --config
```

This will guide you through:
- **WebUI Base URL**: Default is `https://ai.corp.azion.com` (press Enter for default)
- **API Key**: Your authentication key (optional, leave empty if not required)
- **Default Model**: The model to use when none is specified (fetches available models)
- **System Prompt File**: Path to custom system prompt (advanced users)

Configuration is stored in `$HOME/.azion/.aicorp.env` for system-wide access.

### Manual Configuration

Alternatively, you can manually create the configuration file at `$HOME/.azion/.aicorp.env`:
```bash
# Create the Azion config directory
mkdir -p ~/.azion

# Edit the configuration file
nano ~/.azion/.aicorp.env
```

Configuration file format:
```bash
# AI Corp WebUI API configuration
WEBUI_BASE_URL=https://ai.corp.azion.com
WEBUI_API_KEY=your_api_key_here

# Default model to use when none is specified
DEFAULT_MODEL=Azion Copilot

# System prompt file path (relative to project root or absolute path)
SYSTEM_PROMPT_FILE=config/system_prompt.txt
```

**Note**: The system also supports legacy `.env` files in the project directory for backward compatibility.

### System Prompt Customization

The AI Corp client uses a customizable system prompt loaded from a file. This allows you to:

- **Customize AI behavior**: Modify the `config/system_prompt.txt` file to change how the AI responds
- **Platform-aware responses**: The system prompt automatically includes your platform information
- **Easy updates**: Change the system prompt without modifying code

The system prompt file supports template variables:
- `{platform_info}`: Automatically replaced with your OS information

**Example system prompt structure:**
```
You are an AI assistant expert in creating scripts for {platform_info}.
[Your custom instructions here...]
```

## Usage

### Command Line Interface
```bash
# Interactive configuration setup
aicorp --config

# Show available AI Corp models
aicorp --list-models

# Send a prompt with default model
aicorp "Explain quantum computing"

# Send a prompt with specific model
aicorp --model "Azion Copilot" "Hello, world!"

# Verbose output for debugging
aicorp -vvv "Debug this"
```

### Python API
```python
from aicorp import AiCorpClient, Config

# Initialize client
config = Config()
client = AiCorpClient(config)

# Send a prompt
response = client.send_prompt("What is machine learning?")
print(response)
```

## Development

### Running Tests
```bash
pytest
```

### Running Examples
```bash
python examples/basic_usage.py
```

## Key Features

### 🚀 Installation & Setup
- **Smart Environment Detection**: Automatically detects virtual environments vs system installations
- **Interactive PATH Configuration**: Offers to automatically add aicorp to your shell configuration
- **Shell-Aware Instructions**: Provides tailored setup commands for zsh, bash, and other shells
- **Pip Version Management**: Automatically upgrades pip for modern Python packaging support
- **LibreSSL Compatibility**: Fixed urllib3 compatibility issues on macOS systems

### 🛠️ System Management
- **Comprehensive Uninstall**: Complete removal with optional cleanup of configs and cache
- **PATH Analysis**: Detects and warns about shell configuration modifications
- **Dependency Management**: Proper version constraints for stable operation
- **Cross-Platform Support**: Works on macOS with system Python and virtual environments

## AI Corp WebUI API Features

The AI Corp client (`api_client.py`) provides comprehensive text generation capabilities:

### Text Generation
- **Simple Prompts**: Send text prompts with customizable parameters
- **Chat Conversations**: Support for multi-turn conversations with system, user, and assistant roles
- **Configurable Parameters**: Control temperature, max_tokens, top_p, top_k, repetition_penalty, and more

### Model Management
- **Model Listing**: Fetch available models from the AI Corp WebUI API
- **Dynamic Configuration**: Support for different AI Corp endpoints and authentication

### Example Usage in Code
```python
from config import Config
from api_client import AiCorpClient

# Initialize client
config = Config()
client = AiCorpClient(config)

# Simple prompt
response = client.send_prompt("What is machine learning?", max_tokens=100)

# Chat conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain neural networks."}
]
response = client.send_chat_prompt(messages)

# Get available models
models = client.get_models()
```

## Benefits of Modularization

- **Separation of Concerns**: Each module has a single responsibility
- **Reusability**: Modules can be imported and used independently
- **Testability**: Individual components can be tested in isolation
- **Maintainability**: Changes to one module don't affect others
- **Readability**: Clean, focused code that's easy to understand
