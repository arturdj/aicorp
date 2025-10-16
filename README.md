# AI Corp WebUI API Client

A modern, well-structured Python client for interacting with AI Corp's WebUI API service for model management and text generation.

## Project Structure

```
├── src/
│   └── aicorp/
│       ├── __init__.py        # Package initialization
│       ├── api_client.py      # AI Corp WebUI API client implementation
│       ├── config.py          # Configuration management
│       ├── logger.py          # Logging configuration
│       └── cli.py             # Command-line interface
├── tests/
│   ├── __init__.py            # Test package initialization
│   ├── test_api_client.py     # API client tests
│   └── test_config.py         # Configuration tests
├── docs/
│   └── README.md              # Documentation
├── examples/
│   └── basic_usage.py         # Usage examples
├── aicorp                     # Main CLI entry point
├── pyproject.toml             # Modern Python packaging configuration
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── .gitignore                 # Git ignore patterns
└── README.md                  # This file
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

### Option 1: Development Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd aicorp-client
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

### Option 2: Direct Installation
```bash
pip install aicorp-client
```

### Option 3: From Source
```bash
pip install -r requirements.txt
```

## Configuration

Configure environment variables in `.env`:
```bash
# AI Corp WebUI API configuration
WEBUI_BASE_URL=https://ai.corp.azion.com
WEBUI_API_KEY=your_api_key_here
```

## Usage

### Command Line Interface
```bash
# Show available AI Corp models
aicorp --list-models

# Send a prompt with default model
aicorp --prompt "Explain quantum computing"

# Send a prompt with specific model
aicorp --model "Azion Copilot" --prompt "Hello, world!"

# Verbose output for debugging
aicorp -vvv --prompt "Debug this"
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
