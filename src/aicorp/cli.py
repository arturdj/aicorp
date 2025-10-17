#!/usr/bin/env python3
"""AI Corp WebUI API client - Command-line interface module."""

import argparse
import textwrap
import shutil
import threading
import time
import sys
from datetime import datetime
from .config import Config
from .api_client import AiCorpClient
from .logger import setup_logger
from .config_manager import ConfigManager

# ANSI color codes for terminal output
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Text colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_GREY = '\033[100m'
    BG_DARK_BLUE = '\033[104m'


class ProgressIndicator:
    """Animated progress indicator for long-running operations."""
    
    def __init__(self, message="Processing"):
        self.message = message
        self.running = False
        self.thread = None
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.current_char = 0
    
    def _animate(self):
        """Animation loop that runs in a separate thread."""
        while self.running:
            char = self.spinner_chars[self.current_char]
            sys.stdout.write(f'\r{Colors.CYAN}{char} {self.message}...{Colors.RESET}')
            sys.stdout.flush()
            self.current_char = (self.current_char + 1) % len(self.spinner_chars)
            time.sleep(0.1)
    
    def start(self):
        """Start the progress indicator."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._animate, daemon=True)
            self.thread.start()
    
    def stop(self):
        """Stop the progress indicator and clear the line."""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join(timeout=0.2)
            # Clear the progress line
            sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
            sys.stdout.flush()


def get_terminal_width():
    """Get current terminal width, fallback to 80 if unable to detect."""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80


def format_ai_response(response_data, prompt, model=None, interaction_time=None):
    """Format AI response with compact, CLI-friendly output."""
    if not response_data or not isinstance(response_data, dict):
        return
    
    # Extract response content
    choices = response_data.get('choices', [])
    if not choices:
        print(f"{Colors.RED}❌ No response content found{Colors.RESET}")
        return
    
    message = choices[0].get('message', {})
    content = message.get('content', '')
    usage = response_data.get('usage', {})
    model_name = response_data.get('model', model or 'Unknown')
    
    # Get terminal width for dynamic formatting
    term_width = get_terminal_width()
    
    # Compact metadata line (model + usage stats + timestamp)
    timestamp = datetime.now().strftime("%H:%M:%S")
    total_tokens = usage.get('total_tokens', 0) if usage else 0
    
    # Create compact info line with timing
    time_str = f" | {interaction_time:.2f}s" if interaction_time else ""
    if total_tokens > 0:
        info_line = f"{Colors.DIM}[{model_name}] {total_tokens:,} tokens{time_str} | {timestamp}{Colors.RESET}"
    else:
        info_line = f"{Colors.DIM}[{model_name}]{time_str} | {timestamp}{Colors.RESET}"
    
    print(f"\n{info_line}")
    print(f"{Colors.CYAN}{'─' * min(term_width, 80)}{Colors.RESET}")
    
    # Response content with dynamic wrapping
    content_lines = content.split('\n')
    in_code_block = False
    
    for line in content_lines:
        # Check for code block markers
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                # Start of code block - minimal header
                print(f"{Colors.WHITE}{Colors.BOLD}Command:{Colors.RESET} {Colors.DIM}(triple click to select and cmd + c to copy){Colors.RESET}")
                print()
            else:
                # End of code block - just a separator
                print()
            continue
        
        if in_code_block:
            # Format command lines for easy copying
            clean_line = line.strip()
            if clean_line:
                print(f"{Colors.BOLD}{Colors.BRIGHT_BLUE}{clean_line}{Colors.RESET}")
            else:
                print()
        else:
            # Regular text with dynamic wrapping
            if line.strip():  # Skip empty lines in regular text
                # Use terminal width minus small margin for wrapping
                wrap_width = min(term_width - 4, 120)
                if len(line) > wrap_width:
                    wrapped_lines = textwrap.fill(line, width=wrap_width)
                    print(f"{Colors.WHITE}{wrapped_lines}{Colors.RESET}")
                else:
                    print(f"{Colors.WHITE}{line}{Colors.RESET}")
            else:
                print()
    
    print(f"{Colors.CYAN}{'─' * min(term_width, 80)}{Colors.RESET}\n")


def show_models(config, verbosity=2):
    """Fetch and display available AI Corp models in table format."""
    logger = setup_logger(__name__, verbosity=verbosity)
    
    client = AiCorpClient(config, verbosity=verbosity)
    
    # Get raw response to access full model data
    progress = ProgressIndicator("Fetching models")
    progress.start()
    
    try:
        import requests
        response = requests.get(
            url=config.models_endpoint,
            headers=config.headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            models_data = result.get("data", [])
            
            if models_data:
                term_width = get_terminal_width()
                separator_width = min(term_width, 80)
                
                print(f"\n{Colors.CYAN}Available Models ({len(models_data)} total):{Colors.RESET}")
                print(f"{Colors.CYAN}{'─' * separator_width}{Colors.RESET}")
                
                for model in models_data:
                    model_id = model.get("id", "N/A")
                    model_name = model.get("name", model_id)  # Fallback to ID if no name
                    owner = model.get("owned_by", "N/A")
                    
                    # Compact single-line format
                    if model_name != model_id:
                        print(f"{Colors.WHITE}{model_id}{Colors.RESET} {Colors.DIM}({model_name}){Colors.RESET}")
                    else:
                        print(f"{Colors.WHITE}{model_id}{Colors.RESET}")
                
                print(f"{Colors.CYAN}{'─' * separator_width}{Colors.RESET}")
                print(f"{Colors.DIM}Usage: aicorp --model \"<Model ID>\" \"Your prompt\"{Colors.RESET}")
                
                # Return just the IDs for compatibility
                return [model.get("id", "") for model in models_data]
            else:
                print("No models found in response")
                return None
        else:
            print(f"Failed to fetch AI Corp models (Status: {response.status_code})")
            return None
            
    except Exception as e:
        logger.error(f"Error fetching models: {str(e)}")
        print("Failed to fetch AI Corp models")
        return None
    finally:
        progress.stop()


def send_prompt(config, prompt, model=None, verbosity=2):
    """Send a prompt to AI Corp WebUI API with optional model selection."""
    logger = setup_logger(__name__, verbosity=verbosity)
    
    client = AiCorpClient(config, verbosity=verbosity)
    
    # If model is specified, validate it exists
    if model:
        available_models = client.get_models()
        if available_models and model not in available_models:
            print(f"Error: Model '{model}' not found in available_models.")
            return "invalid_model"
    
    # Start timing the interaction
    start_time = time.time()
    
    # Show progress indicator during API call
    progress = ProgressIndicator("Asking {} for help...".format(model))
    progress.start()
    
    try:
        response = client.send_prompt(prompt, model=model)
    finally:
        progress.stop()
    
    # Calculate interaction time
    interaction_time = time.time() - start_time
    
    if response:
        # Use beautiful formatting for the response with timing
        format_ai_response(response, prompt, model, interaction_time)
        return True
    else:
        print(f"{Colors.RED}❌ Failed to get response from AI Corp WebUI API{Colors.RESET}")
        return False


def create_parser(default_model="Azion Copilot"):
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="AI Corp WebUI API client for model management and text generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --config                           # Interactive configuration setup
  %(prog)s --list-models                      # Show available AI Corp models
  %(prog)s "Hello, world!"                    # Send prompt with default model
  %(prog)s --model gpt-3.5 "Hi!"              # Send prompt with specific model
  %(prog)s -v "Hello!"                        # Send prompt with verbose logging
  %(prog)s -vvv --list-models                 # Show models with debug logging
        """
    )
    
    # Add positional argument for prompt
    parser.add_argument(
        'prompt',
        nargs='?',
        type=str,
        help='Prompt to send to the AI Corp WebUI API'
    )
    
    parser.add_argument(
        '-l',
        '--list-models',
        action='store_true',
        help='Show available AI Corp models'
    )
    
    parser.add_argument(
        '--config',
        action='store_true',
        help='Interactive configuration setup for .env file'
    )
    
    parser.add_argument(
        '-m',
        '--model',
        type=str,
        default=default_model,
        help=f'Specify the model to use for generation (default: {default_model})'
    )
    
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='Increase verbosity level (use -v, -vv, -vvv for different levels: ERROR, WARNING, INFO, DEBUG)'
    )
    
    return parser


def main():
    """Main function with command-line interface."""
    # First, parse arguments to check for config command
    # We need to handle config separately since it might run before .env exists
    parser = create_parser()  # Use default model for now
    args = parser.parse_args()
    
    # Handle config command first (doesn't require existing config)
    if args.config:
        config_manager = ConfigManager()
        success = config_manager.interactive_setup()
        if success:
            print(f"\n{Colors.GREEN}✓ Configuration complete! You can now use aicorp commands.{Colors.RESET}")
        return
    
    # For all other commands, load the config
    try:
        config = Config()
        # Re-create parser with actual default model from config
        parser = create_parser(default_model=config.default_model)
        args = parser.parse_args()
        logger = setup_logger(__name__, verbosity=args.verbose)
    except ValueError as e:
        # Handle config loading errors (e.g., missing WEBUI_BASE_URL)
        print(f"{Colors.RED}Configuration error: {str(e)}{Colors.RESET}")
        print(f"{Colors.DIM}Run 'aicorp --config' to set up your configuration{Colors.RESET}")
        return
    except Exception as e:
        # Handle other initialization errors
        print(f"{Colors.RED}Initialization error: {str(e)}{Colors.RESET}")
        return
    
    try:
        
        logger.info("Script started - AI Corp WebUI API client initialized")
        
        # Validate model option usage - only check if model was explicitly provided
        # We need to check if model was explicitly set (not just using default)
        if args.model != config.default_model and not args.prompt:
            print("Error: --model option requires a prompt to be specified")
            parser.print_help()
            return
        
        # Handle commands with unified show_models logic
        show_models_needed = args.list_models
        executed_command = args.list_models or args.config
        
        if args.prompt:
            result = send_prompt(config, args.prompt, args.model, verbosity=args.verbose)
            if result == "invalid_model":
                show_models_needed = True
            executed_command = bool(result)
        
        # Show models if needed (consolidates duplicate calls)
        if show_models_needed:
            show_models(config, verbosity=args.verbose)
            executed_command = True
        
        # Show help if no command was executed
        if not executed_command:
            parser.print_help()
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user (Ctrl+C){Colors.RESET}")
        logger.info("Operation cancelled by user")
        return
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        print(f"Unexpected error: {str(e)}")
    
    logger.info("Script execution completed")


if __name__ == "__main__":
    main()
