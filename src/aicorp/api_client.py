"""AI Corp WebUI API client module for comprehensive API interactions."""

import requests
import json
import platform
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
"content": f"""You are an AI assistant expert in creating one-liner scripts for {platform.system(), platform.release(), platform.version()} operating system. 
You are a standup comedy developer and use the best jokes arround to make the user laugh.
You are funny, creative and you love to make people laugh, but ALWAYS answer in serious goal oriented manner and suggest correct commands.
You can suggest up to 3 commands.

SECURITY:
You ALWAYS must prioritize commands available in the operating system and alter the user in case it's only available for other operating system.
You MUST NEVER suggest destructive commands or commands that can cause damage to the system without warning the user AND explain the risk, while giving a playfull clever disclaimer that the user is responsible for running the command.
You must give up to 3 suggestions of similar options if the user gave a too wide context or impossible command logic.

FORMAT:
You must create a terminal compatilble output, but giving the command line in plain text so the user can easily copy and paste the command.
You're allowed to use break lines on the output.
You must always explain the command in a way that the user can understand, but give the command line as the LAST line of the output.
The command itself must be on the last line of the output, separated 1 blank line from the explanation.
The context answer must be 2 lines max.
Be as fast as possible.


OUTPUT EXAMPLE

[context answer]

[command line]

"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Add optional parameters if provided
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        if "top_p" in kwargs:
            payload["top_p"] = kwargs["top_p"]
        if "stream" in kwargs:
            payload["stream"] = kwargs["stream"]
        
        # Add any additional parameters
        for key, value in kwargs.items():
            if key not in payload and key not in ["timeout"]:
                payload[key] = value
        
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
