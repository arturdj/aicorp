"""Configuration module for AI Corp WebUI API client."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for AI Corp WebUI API client."""
    
    def __init__(self):
        # AI Corp WebUI API configuration
        self.base_url = os.getenv("WEBUI_BASE_URL")
        self.api_key = os.getenv("WEBUI_API_KEY")
        
        if not self.base_url:
            raise ValueError("WEBUI_BASE_URL environment variable is required")
    
    @property
    def headers(self):
        """Get headers for AI Corp WebUI API requests."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    @property
    def models_endpoint(self):
        """Get the AI Corp WebUI models API endpoint."""
        return f"{self.base_url}/api/v1/models"
    
    @property
    def generate_endpoint(self):
        """Get the AI Corp WebUI text generation API endpoint."""
        return f"{self.base_url}/api/chat/completions"
