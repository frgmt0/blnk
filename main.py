from colorama import init, Fore, Back, Style                                                                   
from core.chat_manager import ChatManager                                                                      
from ui.display import Display                                                                                 
                                                                                                                
def main():                                                                                                    
    init()  # Initialize colorama                                                                              
    display = Display()                                                                                        
    chat_manager = ChatManager()                                                                               
                                                                                                                
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
