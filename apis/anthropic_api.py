import os
from anthropic import Anthropic
from .base_api import BaseAPI

class AnthropicAPI(BaseAPI):
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-opus-20240229"
        
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
