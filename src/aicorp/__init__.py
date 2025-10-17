"""AI Corp WebUI API client package."""

__version__ = "1.2.0"
__author__ = "@arturdj"
__description__ = "A Python client for interacting with AI Corp's WebUI API service"

from .api_client import AiCorpClient
from .config import Config
from .logger import setup_logger
from .config_manager import ConfigManager

__all__ = ["AiCorpClient", "Config", "setup_logger", "ConfigManager"]
