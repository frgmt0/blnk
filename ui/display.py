from .colors import Colors                                                                                     
                                                                                                                
class Display:                                                                                                 
    def show_welcome(self):                                                                                    
        print(f"""
{Colors.PRIMARY}╔══════════════════════════════════════╗
║           Welcome to blnk!            ║
╚══════════════════════════════════════╝{Colors.RESET}

{Colors.SECONDARY}A modular terminal chat application supporting multiple AI providers{Colors.RESET}

{Colors.WARNING}Quick Start:{Colors.RESET}
1. Use {Colors.PRIMARY}/apis{Colors.RESET} to see available AI providers
2. Use {Colors.PRIMARY}/use <api_name>{Colors.RESET} to select a provider
3. Use {Colors.PRIMARY}/model-list{Colors.RESET} to see available models
4. Start chatting!

Type {Colors.PRIMARY}/help{Colors.RESET} for detailed command information
""")                                                                                           
                                                                                                            
    def show_response(self, response):                                                                         
        print(f"{Colors.PRIMARY}{response}{Colors.RESET}")                                                     
                                                                                                            
    def show_error(self, error):                                                                               
        print(f"{Colors.ERROR}Error: {error}{Colors.RESET}")
