from .colors import Colors                                                                                     
                                                                                                                
class Display:                                                                                                 
    def show_welcome(self):                                                                                    
        print(f"""                                                                                             
{Colors.PRIMARY}Welcome to blnk!{Colors.RESET}                                                                 
{Colors.SECONDARY}A modular terminal chat application{Colors.RESET}                                            
Use /apis to see available APIs
Type /help for available commands                                                                             
""")                                                                                                           
                                                                                                            
    def show_response(self, response):                                                                         
        print(f"{Colors.PRIMARY}{response}{Colors.RESET}")                                                     
                                                                                                            
    def show_error(self, error):                                                                               
        print(f"{Colors.ERROR}Error: {error}{Colors.RESET}")
