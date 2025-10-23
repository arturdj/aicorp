"""Configuration management module for interactive .env file setup."""

import os
import re
import sys
import termios
import tty
from typing import Dict, Optional, List


class InteractiveModelSelector:
    """Interactive model selector with search and arrow key navigation."""
    
    def __init__(self, models: List[str], current_model: Optional[str] = None):
        """Initialize the selector with available models."""
        self.all_models = models
        self.current_model = current_model
        self.search_term = ""
        self.filtered_models = models.copy()
        self.selected_index = 0
        
        # Find current model index if it exists
        if current_model and current_model in models:
            self.selected_index = models.index(current_model)
    
    def _get_char(self):
        """Get a single character from stdin without pressing Enter."""
        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except (termios.error, OSError):
            # Fallback for environments where termios doesn't work
            return input()
    
    def _filter_models(self):
        """Filter models based on search term."""
        if not self.search_term:
            self.filtered_models = self.all_models.copy()
        else:
            search_lower = self.search_term.lower()
            self.filtered_models = [
                model for model in self.all_models 
                if search_lower in model.lower()
            ]
        
        # Reset selection if current selection is out of bounds
        if self.selected_index >= len(self.filtered_models):
            self.selected_index = max(0, len(self.filtered_models) - 1)
    
    def _display_models(self):
        """Display the current list of models with highlighting."""
        from .cli import Colors
        
        # Clear screen and move cursor to top
        print('\033[2J\033[H', end='')
        
        print(f"{Colors.BOLD}{Colors.BLUE}🔍 Select Default Model{Colors.RESET}")
        print(f"{Colors.DIM}Use ↑/↓ to navigate, type to search, Enter to select, Esc to cancel{Colors.RESET}\n")
        
        # Show search bar
        search_display = self.search_term if self.search_term else ""
        print(f"Search: {Colors.WHITE}{search_display}█{Colors.RESET}")
        print(f"{Colors.DIM}{'─' * 50}{Colors.RESET}")
        
        # Show filtered models
        if not self.filtered_models:
            print(f"{Colors.RED}No models found matching '{self.search_term}'{Colors.RESET}")
            return
        
        # Display up to 10 models at a time
        start_idx = max(0, self.selected_index - 5)
        end_idx = min(len(self.filtered_models), start_idx + 10)
        
        for i in range(start_idx, end_idx):
            model = self.filtered_models[i]
            prefix = "  "
            
            if i == self.selected_index:
                # Highlighted selection
                print(f"{Colors.CYAN}► {model}{Colors.RESET}")
            elif model == self.current_model:
                # Current model indicator
                print(f"{Colors.GREEN}✓ {model} {Colors.DIM}(current){Colors.RESET}")
            else:
                print(f"  {model}")
        
        # Show navigation hint if there are more models
        if len(self.filtered_models) > 10:
            shown = end_idx - start_idx
            total = len(self.filtered_models)
            print(f"\n{Colors.DIM}Showing {shown} of {total} models{Colors.RESET}")
    
    def select_model(self) -> Optional[str]:
        """Run the interactive model selection and return the selected model."""
        if not self.all_models:
            return None
        
        self._filter_models()
        
        while True:
            self._display_models()
            
            try:
                char = self._get_char()
                
                # Handle special keys
                if char == '\x1b':  # Escape sequence
                    # Read the next two characters for arrow keys
                    next_chars = sys.stdin.read(2) if sys.stdin.isatty() else ''
                    if next_chars == '[A':  # Up arrow
                        if self.filtered_models and self.selected_index > 0:
                            self.selected_index -= 1
                    elif next_chars == '[B':  # Down arrow
                        if self.filtered_models and self.selected_index < len(self.filtered_models) - 1:
                            self.selected_index += 1
                    else:
                        # Just Escape key - cancel
                        print('\033[2J\033[H', end='')  # Clear screen
                        return None
                
                elif char == '\r' or char == '\n':  # Enter
                    if self.filtered_models and 0 <= self.selected_index < len(self.filtered_models):
                        selected_model = self.filtered_models[self.selected_index]
                        print('\033[2J\033[H', end='')  # Clear screen
                        return selected_model
                
                elif char == '\x7f' or char == '\x08':  # Backspace
                    if self.search_term:
                        self.search_term = self.search_term[:-1]
                        self._filter_models()
                
                elif char.isprintable() and len(char) == 1:
                    # Regular character - add to search
                    self.search_term += char
                    self._filter_models()
                
                elif char == '\x03':  # Ctrl+C
                    print('\033[2J\033[H', end='')  # Clear screen
                    raise KeyboardInterrupt
                    
            except KeyboardInterrupt:
                print('\033[2J\033[H', end='')  # Clear screen
                return None
            except Exception:
                # Fallback for any terminal issues
                continue


class ConfigManager:
    """Manages .env file configuration interactively."""
    
    def __init__(self, env_file_path: Optional[str] = None):
        """Initialize ConfigManager with path to .env file."""
        if env_file_path is None:
            # Use default Azion config location
            home_dir = os.path.expanduser("~")
            azion_dir = os.path.join(home_dir, ".azion")
            self.full_env_path = os.path.join(azion_dir, ".aicorp.env")
        else:
            # Support custom path for testing
            if os.path.isabs(env_file_path):
                self.full_env_path = env_file_path
            else:
                self.project_root = self._find_project_root()
                self.full_env_path = os.path.join(self.project_root, env_file_path)
    
    def _find_project_root(self) -> str:
        """Find the project root directory (where .env should be located)."""
        # Start from current working directory
        current_dir = os.getcwd()
        
        # Look for common project indicators
        indicators = ['pyproject.toml', '.git']
        
        # Check current directory and parents
        check_dir = current_dir
        for _ in range(10):  # Limit search depth
            for indicator in indicators:
                if os.path.exists(os.path.join(check_dir, indicator)):
                    return check_dir
            
            parent_dir = os.path.dirname(check_dir)
            if parent_dir == check_dir:  # Reached root
                break
            check_dir = parent_dir
        
        # Fallback to current directory
        return current_dir
    
    def load_existing_config(self) -> Dict[str, str]:
        """Load existing configuration from .env file."""
        config = {}
        
        if os.path.exists(self.full_env_path):
            try:
                with open(self.full_env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Skip comments and empty lines
                        if line and not line.startswith('#'):
                            # Match KEY=VALUE pattern
                            match = re.match(r'^([A-Z_][A-Z0-9_]*)\s*=\s*(.*)$', line)
                            if match:
                                key, value = match.groups()
                                # Remove quotes if present
                                value = value.strip('"\'')
                                config[key] = value
            except Exception as e:
                print(f"Warning: Could not read existing .env file: {e}")
        
        return config
    
    def save_config(self, config: Dict[str, str]) -> bool:
        """Save configuration to .env file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.full_env_path), exist_ok=True)
            
            # Create .env content with proper formatting
            content_lines = [
                "",
                "# AI Corp WebUI API configuration",
                "# AI Corp is the name given to the WebUI service"
            ]
            
            # Add configuration values
            if 'WEBUI_BASE_URL' in config:
                content_lines.append(f"WEBUI_BASE_URL={config['WEBUI_BASE_URL']}")
            
            if 'WEBUI_API_KEY' in config:
                content_lines.append(f"WEBUI_API_KEY={config['WEBUI_API_KEY']}")
            
            content_lines.extend([
                "",
                "# Default model to use when none is specified",
                "# Run `aicorp --list-models` to see available models"
            ])
            
            if 'DEFAULT_MODEL' in config:
                # Quote the model name if it contains spaces
                model_value = config['DEFAULT_MODEL']
                if ' ' in model_value:
                    model_value = f'"{model_value}"'
                content_lines.append(f"DEFAULT_MODEL={model_value}")
            
            content_lines.extend([
                "",
                "# System prompt file path (relative to project root or absolute path)",
                f"SYSTEM_PROMPT_FILE={config.get('SYSTEM_PROMPT_FILE', 'config/system_prompt.txt')}",
                ""
            ])
            
            # Write to file
            with open(self.full_env_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content_lines))
            
            return True
            
        except Exception as e:
            print(f"Error: Could not save .env file: {e}")
            return False
    
    def get_available_models(self) -> Optional[List[str]]:
        """Get available models from the API if possible."""
        try:
            # Try to load config and get models
            from .config import Config
            from .api_client import AiCorpClient
            
            # Load current config (may fail if incomplete)
            current_config = self.load_existing_config()
            
            # Check if we have minimum required config
            if 'WEBUI_BASE_URL' not in current_config or 'WEBUI_API_KEY' not in current_config:
                return None
            
            # Temporarily set environment variables
            os.environ['WEBUI_BASE_URL'] = current_config['WEBUI_BASE_URL']
            os.environ['WEBUI_API_KEY'] = current_config['WEBUI_API_KEY']
            
            config = Config()
            client = AiCorpClient(config, verbosity=0)
            models = client.get_models()
            
            return models if models else None
            
        except Exception:
            # If we can't get models, that's okay
            return None
    
    def interactive_setup(self) -> bool:
        """Run interactive configuration setup."""
        from .cli import Colors
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}🔧 AI Corp Configuration Setup{Colors.RESET}")
        print(f"{Colors.DIM}This will help you configure your .env file for AI Corp WebUI API access.{Colors.RESET}\n")
        
        # Load existing configuration
        existing_config = self.load_existing_config()
        
        # Show current .env file location
        print(f"{Colors.DIM}Configuration file: {self.full_env_path}{Colors.RESET}")
        if os.path.exists(self.full_env_path):
            print(f"{Colors.GREEN}✓ Existing configuration file found{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}! Configuration file will be created{Colors.RESET}")
            # Ensure the .azion directory exists
            azion_dir = os.path.dirname(self.full_env_path)
            if not os.path.exists(azion_dir):
                print(f"{Colors.DIM}  Creating directory: {azion_dir}{Colors.RESET}")
        print()
        
        new_config = {}
        
        # 1. WebUI Base URL
        current_url = existing_config.get('WEBUI_BASE_URL', '')
        default_url = 'https://ai.corp.azion.com'
        
        print(f"{Colors.BOLD}1. WebUI Base URL{Colors.RESET}")
        print(f"{Colors.DIM}   The base URL of your AI Corp WebUI API endpoint{Colors.RESET}")
        print(f"{Colors.DIM}   Default: {default_url}{Colors.RESET}")
        if current_url:
            print(f"{Colors.DIM}   Current: {current_url}{Colors.RESET}")
        
        url_prompt = f"   Enter WebUI Base URL"
        if current_url:
            url_prompt += f" (press Enter to keep current, 'd' for default)"
        else:
            url_prompt += f" (press Enter for default)"
        url_prompt += ": "
        
        new_url = input(url_prompt).strip()
        if new_url:
            if new_url.lower() == 'd':
                new_config['WEBUI_BASE_URL'] = default_url
            else:
                new_config['WEBUI_BASE_URL'] = new_url
        elif current_url:
            new_config['WEBUI_BASE_URL'] = current_url
        else:
            new_config['WEBUI_BASE_URL'] = default_url
        
        print()
        
        # 2. API Key (required)
        current_key = existing_config.get('WEBUI_API_KEY', '')
        print(f"{Colors.BOLD}2. API Key (Required){Colors.RESET}")
        print(f"{Colors.DIM}   Your API key for authentication{Colors.RESET}")
        if current_key:
            masked_key = current_key[:8] + "..." if len(current_key) > 8 else current_key
            print(f"{Colors.DIM}   Current: {masked_key}{Colors.RESET}")
        
        key_prompt = f"   Enter API Key"
        if current_key:
            key_prompt += f" (press Enter to keep current)"
        key_prompt += ": "
        
        new_key = input(key_prompt).strip()
        if new_key:
            new_config['WEBUI_API_KEY'] = new_key
        elif current_key:
            new_config['WEBUI_API_KEY'] = current_key
        else:
            # API Key is required, prompt until provided
            while True:
                print(f"{Colors.RED}   API Key is required and cannot be empty.{Colors.RESET}")
                new_key = input("   Enter API Key: ").strip()
                if new_key:
                    new_config['WEBUI_API_KEY'] = new_key
                    break
        
        print()
        
        # 3. Default Model
        current_model = existing_config.get('DEFAULT_MODEL', 'Azion Copilot')
        print(f"{Colors.BOLD}3. Default Model{Colors.RESET}")
        print(f"{Colors.DIM}   The model to use when none is specified{Colors.RESET}")
        if current_model:
            print(f"{Colors.DIM}   Current: {current_model}{Colors.RESET}")
        
        # Try to get available models
        print(f"{Colors.DIM}   Fetching available models...{Colors.RESET}")
        available_models = self.get_available_models()
        
        if available_models and len(available_models) > 1:
            print(f"{Colors.GREEN}   Found {len(available_models)} available models{Colors.RESET}")
            print(f"{Colors.DIM}   Opening interactive model selector...{Colors.RESET}")
            
            # Use interactive selector
            selector = InteractiveModelSelector(available_models, current_model)
            selected_model = selector.select_model()
            
            if selected_model:
                new_config['DEFAULT_MODEL'] = selected_model
                print(f"{Colors.GREEN}   Selected: {selected_model}{Colors.RESET}")
            else:
                # User cancelled, keep current model
                new_config['DEFAULT_MODEL'] = current_model
                print(f"{Colors.YELLOW}   Selection cancelled, keeping current model: {current_model}{Colors.RESET}")
        
        else:
            # No models available or only one model - use current/default
            if available_models and len(available_models) == 1:
                new_config['DEFAULT_MODEL'] = available_models[0]
                print(f"{Colors.GREEN}   Only one model available: {available_models[0]}{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}   Could not fetch models (will use current/default){Colors.RESET}")
                new_config['DEFAULT_MODEL'] = current_model if current_model else 'Azion Copilot'
        
        print()
        
        # 4. System Prompt File (keep existing or default)
        current_prompt_file = existing_config.get('SYSTEM_PROMPT_FILE', 'config/system_prompt.txt')
        new_config['SYSTEM_PROMPT_FILE'] = current_prompt_file
        
        # 5. Confirmation and save
        print(f"{Colors.BOLD}Configuration Summary:{Colors.RESET}")
        print(f"   WebUI Base URL: {Colors.WHITE}{new_config['WEBUI_BASE_URL']}{Colors.RESET}")
        masked = new_config['WEBUI_API_KEY'][:8] + "..." if len(new_config['WEBUI_API_KEY']) > 8 else new_config['WEBUI_API_KEY']
        print(f"   API Key: {Colors.WHITE}{masked}{Colors.RESET}")
        print(f"   Default Model: {Colors.WHITE}{new_config['DEFAULT_MODEL']}{Colors.RESET}")
        print(f"   System Prompt File: {Colors.DIM}{new_config['SYSTEM_PROMPT_FILE']}{Colors.RESET}")
        print()
        
        confirm = input(f"Save this configuration? [Y/n]: ").strip().lower()
        if confirm in ('', 'y', 'yes'):
            if self.save_config(new_config):
                print(f"\n{Colors.GREEN}✓ Configuration saved to {self.full_env_path}{Colors.RESET}")
                print(f"{Colors.DIM}You can now use: aicorp \"Your prompt here\"{Colors.RESET}")
                return True
            else:
                print(f"\n{Colors.RED}✗ Failed to save configuration{Colors.RESET}")
                return False
        else:
            print(f"\n{Colors.YELLOW}Configuration cancelled{Colors.RESET}")
            return False
