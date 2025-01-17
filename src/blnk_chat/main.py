import os
import asyncio
from colorama import init, Fore, Back, Style
from .core.chat_manager import ChatManager
from .ui.display import Display
from .apis.openai_api import OpenAIAPI
from .apis.anthropic_api import AnthropicAPI
from .apis.gemini_api import GeminiAPI
from .utils.config_loader import ConfigLoader

async def main():
    init()
    # Initialize colorama
    display = Display()
    
    # Load configuration
    config = ConfigLoader.load_config()
    chat_manager = ChatManager(config, display)
    
    # Initialize MCP tools
    await chat_manager.initialize_tools()
    
    # Load config and register APIs with available keys
    config = ConfigLoader.load_config()
    if config and 'api_keys' in config:
        if config['api_keys'].get('OPENAI_API_KEY'):
            chat_manager.register_api("openai", OpenAIAPI())
        if config['api_keys'].get('ANTHROPIC_API_KEY'):
            chat_manager.register_api("anthropic", AnthropicAPI())
        if config['api_keys'].get('GOOGLE_API_KEY'):
            chat_manager.register_api("gemini", GeminiAPI())
        
    display.show_welcome()                                      
    while True:
        try:   
            user_input = display.show_input_prompt()
            if user_input.lower() == 'exit':
                break
            response = await chat_manager.process_input(user_input)
            await display.show_response(response)
        except KeyboardInterrupt:                                                                              
            print("\nGoodbye!")
            break
def run():
    """Entry point for the application."""
    asyncio.run(main())

if __name__ == "__main__":
    run()
