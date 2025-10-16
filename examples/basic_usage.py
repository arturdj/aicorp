#!/usr/bin/env python3
"""Basic usage examples for AI Corp WebUI API client."""

import sys
import os

# Add src directory to Python path for examples
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from aicorp import AiCorpClient, Config


def main():
    """Demonstrate basic usage of the AI Corp client."""
    print("AI Corp WebUI API Client - Basic Usage Examples")
    print("=" * 50)
    
    # Initialize configuration and client
    config = Config()
    client = AiCorpClient(config, verbosity=1)  # Minimal logging
    
    # Example 1: List available models
    print("\n1. Listing available models:")
    models = client.get_models()
    if models:
        print(f"Found {len(models)} models:")
        for i, model in enumerate(models[:5], 1):  # Show first 5
            print(f"  {i}. {model}")
        if len(models) > 5:
            print(f"  ... and {len(models) - 5} more")
    else:
        print("  Failed to retrieve models")
    
    # Example 2: Send a simple prompt
    print("\n2. Sending a simple prompt:")
    prompt = "What is the capital of France?"
    response = client.send_prompt(prompt, model="Azion Copilot")
    
    if response and 'choices' in response:
        content = response['choices'][0]['message']['content']
        print(f"  Prompt: {prompt}")
        print(f"  Response: {content}")
    else:
        print("  Failed to get response")
    
    # Example 3: Chat conversation
    print("\n3. Chat conversation example:")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain Python in one sentence."}
    ]
    
    chat_response = client.send_chat_prompt(messages)
    if chat_response and 'choices' in chat_response:
        content = chat_response['choices'][0]['message']['content']
        print(f"  Chat response: {content}")
    else:
        print("  Failed to get chat response")
    
    print("\n" + "=" * 50)
    print("Examples completed!")


if __name__ == "__main__":
    main()
