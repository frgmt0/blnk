from abc import ABC, abstractmethod
from pathlib import Path

class BaseAPI(ABC):
    def __init__(self):
        self.system_prompt = self._load_prompt("SYSTEM.md")
        self.style_prompt = self._load_prompt("STYLE.md")
        
    def _load_prompt(self, filename):
        """Load prompt from file in project root"""
        prompt_path = Path(__file__).parent.parent / filename
        try:
            with open(prompt_path) as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: {filename} not found")
            return ""

    @abstractmethod
    async def send_message(self, message):
        pass

    @abstractmethod
    def get_name(self):
        pass
        
    @abstractmethod
    def get_available_models(self):
        pass
        
    @abstractmethod
    def set_model(self, model_name):
        pass
