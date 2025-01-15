import os
from openai import OpenAI
from .base_api import BaseAPI

class OpenAIAPI(BaseAPI):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-turbo-preview"
        
    def send_message(self, message):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI API Error: {str(e)}"
            
    def get_name(self):
        return "openai"
