import os
import google.generativeai as genai
from .base_api import BaseAPI
from ..config.models import GEMINI_MODELS

class GeminiAPI(BaseAPI):
    def __init__(self):
        super().__init__()  # Initialize BaseAPI
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_name = GEMINI_MODELS[0]
        self.model = genai.GenerativeModel(self.model_name)
        
    async def send_message(self, message):
        try:
            # Combine prompts and message
            full_prompt = f"{self.system_prompt}\n\n{self.style_prompt}\n\n{message}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Gemini API Error: {str(e)}"
            
    def get_name(self):
        return "gemini"
        
    def get_available_models(self):
        return GEMINI_MODELS
        
    def set_model(self, model_name):
        if model_name in GEMINI_MODELS:
            self.model_name = model_name
            self.model = genai.GenerativeModel(model_name)
            return True
        return False
