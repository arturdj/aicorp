"""Tests for the config module."""

import os
import pytest
from unittest.mock import patch, mock_open
from aicorp.config import Config


class TestConfig:
    """Test cases for Config class."""

    @patch.dict(os.environ, {
        'WEBUI_BASE_URL': 'https://test.example.com',
        'WEBUI_API_KEY': 'test-api-key'
    })
    def test_config_from_environment(self):
        """Test config initialization from environment variables."""
        config = Config()
        
        assert config.base_url == 'https://test.example.com'
        assert config.api_key == 'test-api-key'
        assert config.models_endpoint == 'https://test.example.com/api/models'
        assert config.generate_endpoint == 'https://test.example.com/api/chat/completions'

    @patch.dict(os.environ, {}, clear=True)
    def test_config_defaults(self):
        """Test config with default values when no environment variables are set."""
        config = Config()
        
        assert config.base_url == 'https://ai.corp.azion.com'
        assert config.api_key is None
        assert 'Content-Type' in config.headers
        assert config.headers['Content-Type'] == 'application/json'

    @patch.dict(os.environ, {'WEBUI_API_KEY': 'test-key'})
    def test_config_with_api_key(self):
        """Test config headers when API key is provided."""
        config = Config()
        
        assert 'Authorization' in config.headers
        assert config.headers['Authorization'] == 'Bearer test-key'

    def test_config_endpoints(self):
        """Test endpoint URL construction."""
        config = Config()
        
        assert config.models_endpoint.endswith('/api/models')
        assert config.generate_endpoint.endswith('/api/chat/completions')
