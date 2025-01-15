import os
from colorama import init, Fore, Back, Style
from core.chat_manager import ChatManager
from ui.display import Display
from apis.openai_api import OpenAIAPI
from apis.anthropic_api import AnthropicAPI
from apis.gemini_api import GeminiAPI
from dotenv import load_dotenv
                                                                                                                
def main():                                                                                                    
    init()  # Initialize colorama                                                                              
    display = Display()                                                                                        
    load_dotenv()  # Load environment variables
    
    chat_manager = ChatManager()
    
    # Only register APIs with available keys
    if os.getenv("OPENAI_API_KEY"):
        chat_manager.register_api("openai", OpenAIAPI())
    if os.getenv("ANTHROPIC_API_KEY"):
        chat_manager.register_api("anthropic", AnthropicAPI())
    if os.getenv("GOOGLE_API_KEY"):
        chat_manager.register_api("gemini", GeminiAPI())
                                                                                                                
    display.show_welcome()                                                                                     
                                                                                                                
    while True:                                                                                                
        try:                                                                                                   
            user_input = input(f"{Fore.GREEN}blnk>{Style.RESET_ALL} ")                                         
            if user_input.lower() == 'exit':                                                                   
                break                                                                                          
                                                                                                                
            response = chat_manager.process_input(user_input)                                                  
            display.show_response(response)                                                                    
                                                                                                                
        except KeyboardInterrupt:                                                                              
            print("\nGoodbye!")                                                                                
            break                                                                                              
                                                                                                                
if __name__ == "__main__":                                                                                     
    main()                                                                                                     
