"""AI Corp WebUI API client module for comprehensive API interactions."""

import requests
import json
from typing import Dict, Any, Optional, List
from .config import Config
from .logger import setup_logger


class AiCorpClient:
    """AI Corp WebUI API client for model management and text generation."""
    
    def __init__(self, config: Config, verbosity: int = 2):
        self.config = config
        self.logger = setup_logger(__name__, verbosity=verbosity)
    
    def get_models(self) -> Optional[List[str]]:
        """Fetch available models from AI Corp WebUI API.
        
        Returns:
            List of model names or None if request failed
        """
        self.logger.info("Fetching available models from AI Corp WebUI API...")
        self.logger.info(f"Preparing API request to: {self.config.models_endpoint}")
        self._log_headers()
        
        try:
            response = requests.get(
                url=self.config.models_endpoint,
                headers=self.config.headers,
                timeout=10
            )
            
            self.logger.info(f"Response status code: {response.status_code}")
            self.logger.debug(f"Response headers: {dict(response.headers)}")
            self.logger.debug(f"Response payload: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                models = [model.get("id", "") for model in result.get("data", [])]
                self.logger.info(f"Found {len(models)} available models")
                self.logger.debug(f"Response data: {json.dumps(result, indent=2)}")
                return models
            else:
                self.logger.error(f"API request failed with status code: {response.status_code}")
                self.logger.error(f"Error response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request exception occurred: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON response: {str(e)}")
            return None
    
    def send_prompt(self, prompt: str, model: Optional[str] = None, **kwargs) -> Optional[Dict[str, Any]]:
        """Send a prompt to the AI Corp WebUI API for text generation using chat completions format.
        
        Args:
            prompt: The text prompt to send
            model: Optional model name to use for generation
            **kwargs: Additional parameters for the API request
            
        Returns:
            API response data or None if request failed
        """
        # Input validation
        if not prompt or not isinstance(prompt, str):
            self.logger.error("Prompt must be a non-empty string")
            return None
            
        if len(prompt.strip()) == 0:
            self.logger.error("Prompt cannot be empty or whitespace only")
            return None
            
        # Validate model parameter
        if model is not None and not isinstance(model, str):
            self.logger.error("Model must be a string")
            return None
            
        # Sanitize model name (basic validation)
        if model and len(model.strip()) == 0:
            self.logger.warning("Empty model name provided, using default")
            model = None
        
        self.logger.info("Sending prompt to AI Corp WebUI API...")
        self.logger.info(f"Preparing API request to: {self.config.generate_endpoint}")
        self.logger.debug(f"Prompt: {prompt[:100]}..." if len(prompt) > 100 else f"Prompt: {prompt}")
        if model:
            self.logger.info(f"Using model: {model}")
        
        # Use chat completions format
        payload = {
            "model": model or "Azion Copilot",
            "messages": [
                {
                    "role": "system",
                    "content": self.config.system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Add optional parameters if provided (whitelist approach for security)
        ALLOWED_API_PARAMS = {
            'max_tokens', 'temperature', 'top_p', 'stream', 'top_k', 
            'frequency_penalty', 'presence_penalty', 'stop', 'seed'
        }
        
        # Parameter validation ranges
        PARAM_RANGES = {
            'max_tokens': (1, 32768),
            'temperature': (0.0, 2.0),
            'top_p': (0.0, 1.0),
            'top_k': (1, 100),
            'frequency_penalty': (-2.0, 2.0),
            'presence_penalty': (-2.0, 2.0),
        }
        
        validated_params = 0
        for key, value in kwargs.items():
            if key in ALLOWED_API_PARAMS:
                # Validate parameter values
                if key in PARAM_RANGES:
                    min_val, max_val = PARAM_RANGES[key]
                    if not isinstance(value, (int, float)):
                        self.logger.warning(f"Parameter {key} must be numeric, ignoring")
                        continue
                    if not (min_val <= value <= max_val):
                        self.logger.warning(f"Parameter {key}={value} outside valid range [{min_val}, {max_val}], ignoring")
                        continue
                elif key == 'stream' and not isinstance(value, bool):
                    self.logger.warning(f"Parameter {key} must be boolean, ignoring")
                    continue
                elif key == 'stop' and not isinstance(value, (str, list)):
                    self.logger.warning(f"Parameter {key} must be string or list, ignoring")
                    continue
                elif key == 'seed' and not isinstance(value, int):
                    self.logger.warning(f"Parameter {key} must be integer, ignoring")
                    continue
                    
                payload[key] = value
                validated_params += 1
            elif key not in ['timeout']:  # timeout is handled separately
                self.logger.warning(f"Ignoring unsupported parameter: {key}")
                
        self.logger.debug(f"Added {validated_params} validated parameters to payload")
        
        self._log_headers()
        self.logger.debug(f"Request payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(
                url=self.config.generate_endpoint,
                headers=self.config.headers,
                json=payload,
                timeout=kwargs.get("timeout", 30)
            )
            
            self.logger.info(f"Response status code: {response.status_code}")
            self.logger.debug(f"Response headers: {dict(response.headers)}")
            self.logger.debug(f"Response payload: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info("AI Corp WebUI API request successful")
                self.logger.debug(f"Response data: {json.dumps(result, indent=2)}")
                return result
            else:
                self.logger.error(f"AI Corp WebUI API request failed with status code: {response.status_code}")
                self.logger.error(f"Error response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request exception occurred: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON response: {str(e)}")
            return None
    
    def send_chat_prompt(self, messages: List[Dict[str, str]], model: Optional[str] = None, **kwargs) -> Optional[Dict[str, Any]]:
        """Send a chat-style prompt to the AI Corp WebUI API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Optional model name to use for generation
            **kwargs: Additional parameters for the API request
            
        Returns:
            API response data or None if request failed
        """
        # Input validation for messages
        if not messages or not isinstance(messages, list):
            self.logger.error("Messages must be a non-empty list")
            return None
            
        if len(messages) == 0:
            self.logger.error("Messages list cannot be empty")
            return None
        
        # Validate each message structure
        for i, message in enumerate(messages):
            if not isinstance(message, dict):
                self.logger.error(f"Message {i} must be a dictionary")
                return None
            if 'content' not in message:
                self.logger.error(f"Message {i} must have 'content' key")
                return None
            if not isinstance(message['content'], str):
                self.logger.error(f"Message {i} content must be a string")
                return None
            if len(message['content'].strip()) == 0:
                self.logger.error(f"Message {i} content cannot be empty")
                return None
                
        self.logger.info("Sending chat prompt to AI Corp WebUI API...")
        
        # Convert messages to a single prompt string for WebUI
        prompt_parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt = "\n".join(prompt_parts) + "\nAssistant:"
        
        return self.send_prompt(prompt, model=model, **kwargs)
    
    def _log_headers(self):
        """Log request headers (masking sensitive information)."""
        safe_headers = {
            k: v if k not in ['Authorization', 'X-API-Key'] else '***' 
            for k, v in self.config.headers.items()
        }
        self.logger.debug(f"Request headers: {json.dumps(safe_headers, indent=2)}")
