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
    @patch('aicorp.config.Config._load_system_prompt')
    def test_config_from_environment(self, mock_load_prompt):
        """Test config initialization from environment variables."""
        mock_load_prompt.return_value = "Test system prompt"
        config = Config()
        
        assert config.base_url == 'https://test.example.com'
        assert config.api_key == 'test-api-key'
        assert config.models_endpoint == 'https://test.example.com/api/v1/models'
        assert config.generate_endpoint == 'https://test.example.com/api/chat/completions'
        assert config.system_prompt == "Test system prompt"

    @patch.dict(os.environ, {'WEBUI_BASE_URL': 'https://ai.corp.azion.com'}, clear=True)
    @patch('aicorp.config.Config._load_system_prompt')
    def test_config_missing_api_key_raises_error(self, mock_load_prompt):
        """Test config raises error when API key is missing."""
        mock_load_prompt.return_value = "Default system prompt"
        
        with pytest.raises(ValueError, match="WEBUI_API_KEY environment variable is required"):
            Config()

    @patch.dict(os.environ, {}, clear=True)
    @patch('aicorp.config.Config._load_system_prompt')
    def test_config_missing_base_url_raises_error(self, mock_load_prompt):
        """Test config raises error when base URL is missing."""
        mock_load_prompt.return_value = "Default system prompt"
        
        with pytest.raises(ValueError, match="WEBUI_BASE_URL environment variable is required"):
            Config()

    @patch.dict(os.environ, {
        'WEBUI_BASE_URL': 'https://ai.corp.azion.com',
        'WEBUI_API_KEY': 'test-key'
    })
    @patch('aicorp.config.Config._load_system_prompt')
    def test_config_with_api_key(self, mock_load_prompt):
        """Test config headers when API key is provided."""
        mock_load_prompt.return_value = "Test system prompt"
        config = Config()
        
        assert 'Authorization' in config.headers
        assert config.headers['Authorization'] == 'Bearer test-key'

    @patch.dict(os.environ, {
        'WEBUI_BASE_URL': 'https://ai.corp.azion.com',
        'WEBUI_API_KEY': 'test-key'
    })
    @patch('aicorp.config.Config._load_system_prompt')
    def test_config_endpoints(self, mock_load_prompt):
        """Test endpoint URL construction."""
        mock_load_prompt.return_value = "Test system prompt"
        config = Config()
        
        assert config.models_endpoint.endswith('/api/v1/models')
        assert config.generate_endpoint.endswith('/api/chat/completions')

    @patch.dict(os.environ, {
        'WEBUI_BASE_URL': 'https://ai.corp.azion.com',
        'WEBUI_API_KEY': 'test-key',
        'SYSTEM_PROMPT_FILE': 'test_prompt.txt'
    })
    @patch('builtins.open', new_callable=mock_open, read_data="Test prompt for {platform_info}")
    @patch('os.path.exists')
    @patch('platform.system')
    @patch('platform.release')
    @patch('platform.version')
    def test_system_prompt_loading(self, mock_version, mock_release, mock_system, mock_exists, mock_file):
        """Test system prompt loading from file with platform substitution."""
        mock_exists.return_value = True
        mock_system.return_value = "Darwin"
        mock_release.return_value = "21.0.0"
        mock_version.return_value = "Darwin Kernel Version 21.0.0"
        
        config = Config()
        
        assert "Test prompt for Darwin, 21.0.0, Darwin Kernel Version 21.0.0" in config.system_prompt
        mock_file.assert_called_once()

    @patch.dict(os.environ, {
        'WEBUI_BASE_URL': 'https://ai.corp.azion.com',
        'WEBUI_API_KEY': 'test-key',
        'SYSTEM_PROMPT_FILE': 'nonexistent.txt'
    })
    @patch('os.path.exists')
    def test_system_prompt_fallback(self, mock_exists):
        """Test system prompt fallback when file doesn't exist."""
        mock_exists.return_value = False
        
        config = Config()
        
        assert config.system_prompt == "You are a helpful AI assistant that provides accurate and useful responses."

    @patch.dict(os.environ, {
        'WEBUI_BASE_URL': 'https://ai.corp.azion.com',
        'WEBUI_API_KEY': 'test-key',
        'SYSTEM_PROMPT_FILE': 'test_prompt.txt'
    })
    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    @patch('os.path.exists')
    def test_system_prompt_permission_error(self, mock_exists, mock_file):
        """Test system prompt fallback when file cannot be read due to permissions."""
        mock_exists.return_value = True
        
        with patch('builtins.print') as mock_print:
            config = Config()
            
            assert config.system_prompt == "You are a helpful AI assistant that provides accurate and useful responses."
            mock_print.assert_called_once()
            assert "Warning: Could not load system prompt file" in mock_print.call_args[0][0]

    @patch.dict(os.environ, {
        'WEBUI_BASE_URL': 'https://ai.corp.azion.com',
        'WEBUI_API_KEY': 'test-key',
        'SYSTEM_PROMPT_FILE': '/absolute/path/to/prompt.txt'
    })
    @patch('builtins.open', new_callable=mock_open, read_data="Absolute path prompt")
    @patch('os.path.exists')
    def test_system_prompt_absolute_path(self, mock_exists, mock_file):
        """Test system prompt loading with absolute path."""
        mock_exists.return_value = True
        
        config = Config()
        
        assert "Absolute path prompt" in config.system_prompt
        mock_file.assert_called_once_with('/absolute/path/to/prompt.txt', 'r', encoding='utf-8')

    @patch.dict(os.environ, {
        'WEBUI_BASE_URL': 'https://ai.corp.azion.com',
        'WEBUI_API_KEY': 'test-key'
    }, clear=True)
    def test_config_default_values(self):
        """Test config default values."""
        with patch('aicorp.config.Config._load_system_prompt') as mock_load_prompt:
            mock_load_prompt.return_value = "Test system prompt"
            config = Config()
            
            assert config.default_model == "Azion Copilot"
            assert config.system_prompt_file == "config/system_prompt.txt"

    @patch.dict(os.environ, {
        'WEBUI_BASE_URL': 'https://ai.corp.azion.com',
        'WEBUI_API_KEY': 'test-key',
        'DEFAULT_MODEL': 'custom-model'
    })
    def test_config_custom_default_model(self):
        """Test config with custom default model."""
        with patch('aicorp.config.Config._load_system_prompt') as mock_load_prompt:
            mock_load_prompt.return_value = "Test system prompt"
            config = Config()
            
            assert config.default_model == "custom-model"

    @patch.dict(os.environ, {
        'WEBUI_BASE_URL': 'https://test.com/',  # URL with trailing slash
        'WEBUI_API_KEY': 'test-key'
    })
    def test_config_url_with_trailing_slash(self):
        """Test config handles base URL with trailing slash correctly."""
        with patch('aicorp.config.Config._load_system_prompt') as mock_load_prompt:
            mock_load_prompt.return_value = "Test system prompt"
            config = Config()
            
            # Endpoints should handle trailing slash correctly
            assert config.models_endpoint == "https://test.com/api/v1/models"
            assert config.generate_endpoint == "https://test.com/api/chat/completions"
