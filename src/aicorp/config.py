"""Configuration module for AI Corp WebUI API client."""

import os
import platform
from dotenv import load_dotenv

def _get_config_file_path():
    """Get the path to the configuration file."""
    # First try the new Azion config location
    home_dir = os.path.expanduser("~")
    azion_config = os.path.join(home_dir, ".azion", ".aicorp.env")
    
    if os.path.exists(azion_config):
        return azion_config
    
    # Fallback to project-local .env for backward compatibility
    project_env = os.path.join(os.getcwd(), ".env")
    if os.path.exists(project_env):
        return project_env
    
    # Return the preferred location even if it doesn't exist
    return azion_config

# Load environment variables from .env file
config_file = _get_config_file_path()
load_dotenv(config_file)


class Config:
    """Configuration class for AI Corp WebUI API client."""
    
    def __init__(self):
        # AI Corp WebUI API configuration
        self.base_url = os.getenv("WEBUI_BASE_URL")
        self.api_key = os.getenv("WEBUI_API_KEY")
        self.default_model = os.getenv("DEFAULT_MODEL", "Azion Copilot")
        self.system_prompt_file = os.getenv("SYSTEM_PROMPT_FILE", "config/system_prompt.txt")
        
        if not self.base_url:
            raise ValueError("WEBUI_BASE_URL environment variable is required")
        
        if not self.api_key:
            raise ValueError("WEBUI_API_KEY environment variable is required")
        
        # Load system prompt from file
        self.system_prompt = self._load_system_prompt()
    
    @property
    def headers(self):
        """Get headers for AI Corp WebUI API requests."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        return headers
    
    @property
    def models_endpoint(self):
        """Get the AI Corp WebUI models API endpoint."""
        return f"{self.base_url}/api/v1/models"
    
    @property
    def generate_endpoint(self):
        """Get the AI Corp WebUI text generation API endpoint."""
        return f"{self.base_url}/api/chat/completions"
    
    def _load_system_prompt(self):
        """Load system prompt from file with platform info substitution."""
        try:
            # Try relative path first, then absolute path
            if not os.path.isabs(self.system_prompt_file):
                # Look for file relative to project root (where .env is located)
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                prompt_file_path = os.path.join(project_root, self.system_prompt_file)
            else:
                prompt_file_path = self.system_prompt_file
            
            if not os.path.exists(prompt_file_path):
                raise FileNotFoundError(f"System prompt file not found: {prompt_file_path}")
            
            with open(prompt_file_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read().strip()
            
            # Substitute platform information
            platform_info = f"{platform.system()}, {platform.release()}, {platform.version()}"
            system_prompt = prompt_template.format(platform_info=platform_info)
            
            return system_prompt
            
        except Exception as e:
            # Fallback to a basic system prompt if file loading fails
            fallback_prompt = "You are a helpful AI assistant that provides accurate and useful responses."
            print(f"Warning: Could not load system prompt file ({e}). Using fallback prompt.")
            return fallback_prompt
