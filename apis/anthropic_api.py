import os
from anthropic import Anthropic
from .base_api import BaseAPI
from config.models import ANTHROPIC_MODELS

class AnthropicAPI(BaseAPI):
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = ANTHROPIC_MODELS[0]
        
    def send_message(self, message):
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": message}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Anthropic API Error: {str(e)}"
            
    def get_name(self):
        return "anthropic"
        
    def get_available_models(self):
        return ANTHROPIC_MODELS
        
    def set_model(self, model_name):
        if model_name in ANTHROPIC_MODELS:
            self.model = model_name
            return True
        return False
