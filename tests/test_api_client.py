"""Tests for the API client module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
from aicorp.api_client import AiCorpClient
from aicorp.config import Config


class TestAiCorpClient:
    """Test cases for AiCorpClient class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = Mock(spec=Config)
        self.config.models_endpoint = "https://test.com/api/models"
        self.config.generate_endpoint = "https://test.com/api/chat/completions"
        self.config.headers = {"Content-Type": "application/json"}
        self.config.system_prompt = "You are a helpful AI assistant."
        
        self.client = AiCorpClient(self.config, verbosity=0)

    @patch('aicorp.api_client.requests.get')
    def test_get_models_success(self, mock_get):
        """Test successful model retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
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
        mock_response.text = "Not found"
        mock_get.return_value = mock_response

        models = self.client.get_models()

        assert models is None

    @patch('aicorp.api_client.requests.post')
    def test_send_prompt_success(self, mock_post):
        """Test successful prompt sending."""
        mock_response = Mock()
        mock_response.status_code = 200
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
