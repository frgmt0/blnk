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
        elif cmd == 'model-list':
            return self.show_models()
        elif cmd == 'switch-model' and len(parts) > 1:
            return self.switch_model(' '.join(parts[1:]))

        return f"Unknown command: {cmd}"

    def show_models(self):
        if not self.current_api:
            return "No API selected. Please select an API first."
        
        models = self.current_api.get_available_models()
        return f"Available models for {self.current_api.get_name()}:\n" + "\n".join(models)
        
    def switch_model(self, model_name):
        if not self.current_api:
            return "No API selected. Please select an API first."
            
        if self.current_api.set_model(model_name):
            return f"Switched to model: {model_name}"
        return f"Invalid model name for {self.current_api.get_name()}"
