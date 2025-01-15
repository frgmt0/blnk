from apis.base_api import BaseAPI                                                                              
                                                                                                            
class ChatManager:                                                                                             
    def __init__(self):                                                                                        
        self.apis = {}                                                                                         
        self.current_api = None                                                                                
                                                                                                            
    def register_api(self, name, api_instance):                                                                
        if isinstance(api_instance, BaseAPI):                                                                  
            self.apis[name] = api_instance                                                                     
                                                                                                            
    def process_input(self, user_input):                                                                       
        if user_input.startswith('/'):                                                                         
            return self.handle_command(user_input[1:])                                                         
                                                                                                            
        if self.current_api:                                                                                   
            return self.current_api.send_message(user_input)                                                   
        return "No API selected. Use /api <name> to select an API."                                            
                                                                                                            
    def handle_command(self, command):                                                                         
        parts = command.split()                                                                                
        cmd = parts[0].lower()                                                                                 
                                                                                                            
        if cmd == 'help':                                                                                      
            return self.show_help()                                                                            
        elif cmd == 'api' and len(parts) > 1:                                                                  
            return self.switch_api(parts[1])                                                                   
                                                                                                            
        return f"Unknown command: {cmd}"  