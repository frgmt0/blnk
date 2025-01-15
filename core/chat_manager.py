from apis.base_api import BaseAPI                                                                              
                                                                                                            
class ChatManager:                                                                                             
    def __init__(self, config=None):                                                                                        
        self.apis = {}                                                                                         
        self.current_api = None
        self.config = config
                                                                                                            
    def register_api(self, name, api_instance):                                                                
        if isinstance(api_instance, BaseAPI):                                                                  
            self.apis[name] = api_instance
            
            # Set default model if configured
            if self.config and name in self.config['default_models']:
                api_instance.set_model(self.config['default_models'][name])
                
            # Set as current API if it's the default
            if self.config and self.config['default_api'] == name:
                self.current_api = api_instance
                                                                                                            
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
            help_text = f"""
Available Commands:
  /help           Show this help message
  /apis           List available AI providers
  /use <api>      Switch to specified AI provider
  /model-list     Show available models for current/all providers
  /switch-model   Switch to a different model for current provider
  exit            Exit the application

Examples:
  /use openai             Switch to OpenAI provider
  /switch-model gpt-4o    Switch to GPT-4 model
"""
            return help_text
        elif cmd == 'apis':
            return self.show_available_apis()
        elif cmd == 'model-list':
            return self.show_models()
        elif cmd == 'switch-model' and len(parts) > 1:
            return self.switch_model(' '.join(parts[1:]))
        elif cmd == 'use' and len(parts) > 1:
            api_name = parts[1].lower()
            if api_name in self.apis:
                self.current_api = self.apis[api_name]
                return f"Switched to {api_name} API"
            return f"API '{api_name}' not available. Use /apis to see available APIs."

        return f"Unknown command: {cmd}"

    def show_available_apis(self):
        if not self.apis:
            return "No APIs configured. Please add API keys to your .env file."
        return "Available APIs:\n" + "\n".join(f"  {name}" for name in self.apis.keys())

    def show_models(self):
        if not self.apis:
            return "No APIs available. Please add API keys to your .env file."
            
        if not self.current_api:
            # Show all available APIs and their models
            result = "Available models for all configured APIs:\n"
            for api in self.apis.values():
                result += f"\n{api.get_name().upper()}:\n"
                result += "\n".join(f"  {model}" for model in api.get_available_models())
            return result
        
        # Show models for current API
        models = self.current_api.get_available_models()
        return f"Available models for {self.current_api.get_name()}:\n" + "\n".join(f"  {model}" for model in models)
        
    def switch_model(self, model_name):
        if not self.current_api:
            return "No API selected. Please select an API first."
            
        if self.current_api.set_model(model_name):
            return f"Switched to model: {model_name}"
        return f"Invalid model name for {self.current_api.get_name()}"
