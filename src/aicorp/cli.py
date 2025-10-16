#!/usr/bin/env python3
"""AI Corp WebUI API client - Command-line interface module."""

import argparse
import textwrap
import shutil
from datetime import datetime
from .config import Config
from .api_client import AiCorpClient
from .logger import setup_logger

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


def get_terminal_width():
    """Get current terminal width, fallback to 80 if unable to detect."""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80


def format_ai_response(response_data, prompt, model=None):
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
    
    # Create compact info line
    if total_tokens > 0:
        info_line = f"{Colors.DIM}[{model_name}] {total_tokens:,} tokens | {timestamp}{Colors.RESET}"
    else:
        info_line = f"{Colors.DIM}[{model_name}] {timestamp}{Colors.RESET}"
    
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
                print(f"{Colors.WHITE}Command:{Colors.RESET} {Colors.DIM}(triple click to select and cmd + c to copy){Colors.RESET}")
                print()
            else:
                # End of code block - just a separator
                print()
            continue
        
        if in_code_block:
            # Format command lines for easy copying
            clean_line = line.strip()
            if clean_line:
                print(f"{Colors.BRIGHT_YELLOW}{clean_line}{Colors.RESET}")
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
                print(f"{Colors.DIM}Usage: aicorp -m \"<Model ID>\" -p \"Your prompt\"{Colors.RESET}")
                
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


def send_prompt(config, prompt, model=None, verbosity=2):
    """Send a prompt to AI Corp WebUI API with optional model selection."""
    logger = setup_logger(__name__, verbosity=verbosity)
    
    client = AiCorpClient(config, verbosity=verbosity)
    
    # If model is specified, validate it exists
    if model:
        available_models = client.get_models()
        if available_models and model not in available_models:
            print(f"Error: Model '{model}' not found in available models.")
            return "invalid_model"
    
    response = client.send_prompt(prompt, model=model)
    
    if response:
        # Use beautiful formatting for the response
        format_ai_response(response, prompt, model)
        return True
    else:
        print(f"{Colors.RED}❌ Failed to get response from AI Corp WebUI API{Colors.RESET}")
        return False


def create_parser():
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="AI Corp WebUI API client for model management and text generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list-models                      # Show available AI Corp models
  %(prog)s --prompt "Hello, world!"          # Send prompt with default model
  %(prog)s --model gpt-3.5 --prompt "Hi!"    # Send prompt with specific model
  %(prog)s -v --prompt "Hello!"              # Send prompt with verbose logging
  %(prog)s -vvv --list-models                # Show models with debug logging
        """
    )
    
    # Create mutually exclusive group for list-models and prompt
    action_group = parser.add_mutually_exclusive_group()
    
    action_group.add_argument(
        '-l',
        '--list-models',
        action='store_true',
        help='Show available AI Corp models'
    )
    
    action_group.add_argument(
        '-p',
        '--prompt',
        type=str,
        help='Send a prompt to the AI Corp WebUI API'
    )
    
    parser.add_argument(
        '-m',
        '--model',
        type=str,
        default="Azion Copilot",
        help='Specify the model to use for generation'
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
    parser = create_parser()
    args = parser.parse_args()
    logger = setup_logger(__name__, verbosity=args.verbose)
    
    try:
        logger.info("Script started - AI Corp WebUI API client initialized")
        config = Config()
        
        # Validate model option usage - only check if model was explicitly provided
        # We need to check if model was explicitly set (not just using default)
        if args.model != "Azion Copilot" and not args.prompt:
            print("Error: --model option requires --prompt to be specified")
            parser.print_help()
            return
        
        # Handle commands with unified show_models logic
        show_models_needed = args.list_models
        executed_command = args.list_models
        
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
            
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        print(f"Unexpected error: {str(e)}")
    
    logger.info("Script execution completed")


if __name__ == "__main__":
    main()
