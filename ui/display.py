from .colors import Colors                                                                                     
                                                                                                                
class Display:                                                                                                 
    def show_welcome(self):                                                                                    
        print(f"""
{Colors.PRIMARY}╔══════════════════════════════════════╗
║           Welcome to blnk!           ║
╚══════════════════════════════════════╝{Colors.RESET}

{Colors.SECONDARY}A modular terminal chat application supporting multiple AI providers{Colors.RESET}

{Colors.WARNING}Quick Start:{Colors.RESET}
> Use {Colors.PRIMARY}/apis{Colors.RESET} to see available AI providers
> Use {Colors.PRIMARY}/use <api_name>{Colors.RESET} to select a provider
> Use {Colors.PRIMARY}/model-list{Colors.RESET} to see available models
> Use {Colors.PRIMARY}/switch-model <model_name>{Colors.RESET} to switch to a new model
> Start chatting!

Type {Colors.PRIMARY}/help{Colors.RESET} for detailed command information
""")                                                                           
                                                                                                            
    def show_response(self, response):                                                                         
        print(f"{Colors.PRIMARY}{response}{Colors.RESET}")                                                     
                                                                                                            
    def show_error(self, error):                                                                               
        print(f"{Colors.ERROR}Error: {error}{Colors.RESET}")
