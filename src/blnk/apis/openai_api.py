import os
from openai import OpenAI
from .base_api import BaseAPI
from ..config.models import OPENAI_MODELS

class OpenAIAPI(BaseAPI):
    def __init__(self):
        super().__init__()  # Initialize BaseAPI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = OPENAI_MODELS[0]
        
    async def send_message(self, message):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "system", "content": self.style_prompt},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI API Error: {str(e)}"
            
    def get_name(self):
        return "openai"
        
    def get_available_models(self):
        return OPENAI_MODELS
        
    def set_model(self, model_name):
        if model_name in OPENAI_MODELS:
            self.model = model_name
            return True
        return False
