# aicorp-client

Python client library for AI Corp WebUI API.

## Overview

`aicorp-client` provides programmatic access to AI Corp's WebUI API service. The library includes both a Python API and command-line interface for text generation and model management.

## Project Structure

```
aicorp-client/
├── src/aicorp/               # Source code
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Command-line interface
│   ├── api_client.py         # HTTP API client
│   ├── config.py             # Configuration management
│   ├── config_manager.py     # Interactive configuration
│   └── logger.py             # Logging utilities
├── config/                   # Configuration templates
│   └── system_prompt.txt     # Default system prompt
├── scripts/                  # Installation scripts
├── tests/                    # Test suite
├── examples/                 # Usage examples
└── docs/                     # Documentation
```

## Core Components

### API Client (`api_client.py`)
- HTTP client for AI Corp WebUI API
- Supports text generation and chat conversations
- Model listing and management
- Request validation and error handling

### Configuration (`config.py`, `config_manager.py`)
- Environment variable management
- Interactive configuration setup
- API endpoint and authentication handling

### CLI (`cli.py`)
- Command-line interface
- Model selection and management
- Interactive and batch processing modes

## Installation

### Requirements
- Python 3.8+
- pip

### From Source
```bash
git clone <repository-url>
cd aicorp-client
pip install -e .
```

### Using Installation Script
```bash
./scripts/install.sh
```

The installation script handles:
- Python version verification
- Virtual environment detection
- Dependency installation
- PATH configuration
- Environment setup

### From PyPI [not published yet]
```bash
pip install aicorp-client
```

## Configuration

### Interactive Setup
```bash
aicorp --config
```

Configure the following parameters:
- **WEBUI_BASE_URL**: API endpoint (default: `https://ai.corp.azion.com`)
- **WEBUI_API_KEY**: Authentication token (required)
- **DEFAULT_MODEL**: Default model for requests
- **SYSTEM_PROMPT_FILE**: Path to system prompt template

### Manual Configuration

Create configuration file at `$HOME/.azion/.aicorp.env`:

```bash
mkdir -p ~/.azion
```

Configuration format:
```bash
WEBUI_BASE_URL=https://ai.corp.azion.com
WEBUI_API_KEY=your_api_key_here
DEFAULT_MODEL=Azion Copilot
SYSTEM_PROMPT_FILE=config/system_prompt.txt
```

### System Prompt

The system prompt template supports variables:
- `{platform_info}`: Replaced with OS information

Example template:
```
You are an AI assistant for {platform_info}.
[Additional instructions...]
```

## Uninstallation

```bash
./scripts/uninstall.sh
```

Or manually:
```bash
pip uninstall aicorp-client
```

## Usage

### Command Line Interface
```bash
# Configuration
aicorp --config

# List available models
aicorp --list-models

# Send prompt with default model
aicorp "Explain quantum computing"

# Send prompt with specific model
aicorp --model "Azion Copilot" "Hello, world!"

# Verbose output
aicorp -vvv "Debug this"
```

### Python API
```python
from aicorp import AiCorpClient, Config

# Initialize client
config = Config()
client = AiCorpClient(config)

# Send prompt
response = client.send_prompt("What is machine learning?")
print(response)

# Chat conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain neural networks."}
]
response = client.send_chat_prompt(messages)

# List models
models = client.get_models()
```

## API Reference

### AiCorpClient Methods

#### `send_prompt(prompt, **kwargs)`
Send text prompt to API.

**Parameters:**
- `prompt` (str): Input text
- `max_tokens` (int): Maximum response tokens (1-32768)
- `temperature` (float): Sampling temperature (0.0-2.0)
- `top_p` (float): Nucleus sampling parameter (0.0-1.0)

#### `send_chat_prompt(messages, **kwargs)`
Send chat conversation to API.

**Parameters:**
- `messages` (list): List of message dictionaries with 'role' and 'content'
- Additional parameters same as `send_prompt`

#### `get_models()`
Retrieve available models from API.

**Returns:** List of model names

## Development

### Running Tests
```bash
pytest
```

### Running Examples
```bash
python examples/basic_usage.py
```
## Project Structure

```
src/aicorp/
├── __init__.py           # Package initialization
├── cli.py                # Command-line interface
├── api_client.py         # API client with validation
├── config.py             # Configuration management
├── config_manager.py     # Interactive setup
└── logger.py             # Logging utilities