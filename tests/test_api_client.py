"""Tests for the API client module."""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
from aicorp.api_client import AiCorpClient
from aicorp.config import Config


class TestAiCorpClient:
    """Test cases for AiCorpClient class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Use a simple object instead of Mock to avoid dictionary iteration issues
        class MockConfig:
            def __init__(self):
                self.models_endpoint = "https://test.com/api/models"
                self.generate_endpoint = "https://test.com/api/chat/completions"
                self.headers = {"Content-Type": "application/json"}
                self.system_prompt = "You are a helpful AI assistant."
        
        self.config = MockConfig()
        self.client = AiCorpClient(self.config, verbosity=0)

    @patch('aicorp.api_client.requests.get')
    def test_get_models_success(self, mock_get):
        """Test successful model retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "data": [
                {"id": "model1", "name": "Model 1"},
                {"id": "model2", "name": "Model 2"}
            ]
        }
        mock_get.return_value = mock_response

        models = self.client.get_models()

        assert models == ["model1", "model2"]
        mock_get.assert_called_once_with(
            url=self.config.models_endpoint,
            headers=self.config.headers,
            timeout=10
        )

    @patch('aicorp.api_client.requests.get')
    def test_get_models_failure(self, mock_get):
        """Test model retrieval failure."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.text = "Not found"
        mock_get.return_value = mock_response

        models = self.client.get_models()

        assert models is None

    @patch('aicorp.api_client.requests.post')
    def test_send_prompt_success(self, mock_post):
        """Test successful prompt sending."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}],
            "usage": {"total_tokens": 100}
        }
        mock_post.return_value = mock_response

        response = self.client.send_prompt("Test prompt", model="test-model")

        assert response is not None
        assert "choices" in response
        mock_post.assert_called_once()

    @patch('aicorp.api_client.requests.post')
    def test_send_prompt_failure(self, mock_post):
        """Test prompt sending failure."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.text = "Internal server error"
        mock_post.return_value = mock_response

        response = self.client.send_prompt("Test prompt")

        assert response is None

    @patch('aicorp.api_client.requests.post')
    def test_send_prompt_request_exception(self, mock_post):
        """Test prompt sending with request exception."""
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        response = self.client.send_prompt("Test prompt")

        assert response is None

    def test_send_chat_prompt(self):
        """Test chat prompt functionality."""
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        
        with patch.object(self.client, 'send_prompt') as mock_send:
            mock_send.return_value = {"test": "response"}
            
            result = self.client.send_chat_prompt(messages, model="test-model")
            
            mock_send.assert_called_once()
            assert result == {"test": "response"}

    def test_input_validation_empty_prompt(self):
        """Test input validation for empty prompt."""
        result = self.client.send_prompt("")
        assert result is None
        
        result = self.client.send_prompt("   ")
        assert result is None
        
        result = self.client.send_prompt(None)
        assert result is None

    def test_input_validation_invalid_model(self):
        """Test input validation for invalid model."""
        with patch.object(self.client, 'logger') as mock_logger:
            result = self.client.send_prompt("test", model=123)
            assert result is None
            mock_logger.error.assert_called()

    def test_parameter_validation_ranges(self):
        """Test parameter validation with ranges."""
        with patch('aicorp.api_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.json.return_value = {"choices": [{"message": {"content": "Test"}}]}
            mock_post.return_value = mock_response
            
            # Test valid parameters
            result = self.client.send_prompt("test", temperature=0.5, max_tokens=100)
            assert result is not None
            
            # Test invalid parameters (should be ignored)
            with patch.object(self.client, 'logger') as mock_logger:
                result = self.client.send_prompt("test", temperature=5.0, max_tokens=-1)
                assert result is not None
                mock_logger.warning.assert_called()

    def test_chat_input_validation(self):
        """Test input validation for chat messages."""
        # Test empty messages
        result = self.client.send_chat_prompt([])
        assert result is None
        
        result = self.client.send_chat_prompt(None)
        assert result is None
        
        # Test invalid message structure
        result = self.client.send_chat_prompt([{"role": "user"}])  # Missing content
        assert result is None
        
        result = self.client.send_chat_prompt([{"content": ""}])  # Empty content
        assert result is None

    @patch('aicorp.api_client.requests.get')
    def test_get_models_json_decode_error(self, mock_get):
        """Test model retrieval with JSON decode error."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "Invalid JSON response"
        mock_get.return_value = mock_response

        models = self.client.get_models()

        assert models is None

    @patch('aicorp.api_client.requests.get')
    def test_get_models_empty_data(self, mock_get):
        """Test model retrieval with empty data array."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response

        models = self.client.get_models()

        assert models == []

    @patch('aicorp.api_client.requests.get')
    def test_get_models_malformed_data(self, mock_get):
        """Test model retrieval with malformed data structure."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"data": [{"name": "model1"}, {"id": "model2"}]}
        mock_get.return_value = mock_response

        models = self.client.get_models()

        assert models == ["", "model2"]  # Missing id becomes empty string

    @patch('aicorp.api_client.requests.post')
    def test_send_prompt_json_decode_error(self, mock_post):
        """Test prompt sending with JSON decode error in response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "Invalid JSON response"
        mock_post.return_value = mock_response

        response = self.client.send_prompt("Test prompt")

        assert response is None

    def test_send_prompt_with_timeout_parameter(self):
        """Test prompt sending with custom timeout parameter."""
        with patch('aicorp.api_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.json.return_value = {"choices": [{"message": {"content": "Test"}}]}
            mock_post.return_value = mock_response
            
            result = self.client.send_prompt("test", timeout=60)
            
            # Verify timeout was passed correctly
            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args[1]
            assert call_kwargs['timeout'] == 60

    def test_send_prompt_parameter_validation_edge_cases(self):
        """Test parameter validation with edge case values."""
        with patch('aicorp.api_client.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.json.return_value = {"choices": [{"message": {"content": "Test"}}]}
            mock_post.return_value = mock_response
            
            with patch.object(self.client, 'logger') as mock_logger:
                # Test boundary values
                result = self.client.send_prompt("test", temperature=0.0, max_tokens=1)
                assert result is not None
                
                result = self.client.send_prompt("test", temperature=2.0, max_tokens=32768)
                assert result is not None
                
                # Test invalid types
                result = self.client.send_prompt("test", temperature="invalid", max_tokens="invalid")
                assert result is not None
                mock_logger.warning.assert_called()

    def test_chat_prompt_with_system_messages(self):
        """Test chat prompt with system messages."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"}
        ]
        
        with patch.object(self.client, 'send_prompt') as mock_send:
            mock_send.return_value = {"test": "response"}
            
            result = self.client.send_chat_prompt(messages)
            
            # Verify the prompt was constructed correctly
            mock_send.assert_called_once()
            call_args = mock_send.call_args[0]
            prompt = call_args[0]
            
            assert "System: You are a helpful assistant" in prompt
            assert "User: Hello" in prompt
            assert "Assistant: Hi there!" in prompt
            assert "User: How are you?" in prompt
            assert prompt.endswith("Assistant:")

    def test_chat_prompt_invalid_message_types(self):
        """Test chat prompt with various invalid message types."""
        # Test non-dict message
        result = self.client.send_chat_prompt(["invalid_message"])
        assert result is None
        
        # Test message with non-string content
        result = self.client.send_chat_prompt([{"role": "user", "content": 123}])
        assert result is None
        
        # Test message with whitespace-only content
        result = self.client.send_chat_prompt([{"role": "user", "content": "   "}])
        assert result is None

    def test_log_headers_masking(self):
        """Test that sensitive headers are masked in logs."""
        # Set up config with sensitive headers
        self.config.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer secret-key",
            "X-API-Key": "another-secret"
        }
        
        with patch.object(self.client, 'logger') as mock_logger:
            self.client._log_headers()
            
            # Verify logger.debug was called
            mock_logger.debug.assert_called_once()
            logged_message = mock_logger.debug.call_args[0][0]
            
            # Check that sensitive values are masked
            assert "secret-key" not in logged_message
            assert "another-secret" not in logged_message
            assert "***" in logged_message
            assert "application/json" in logged_message
