import os
import google.generativeai as genai
from .base_api import BaseAPI

class GeminiAPI(BaseAPI):
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
        
    def send_message(self, message):
        try:
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            return f"Gemini API Error: {str(e)}"
            
    def get_name(self):
        return "gemini"
