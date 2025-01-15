import os
from anthropic import AsyncAnthropic
from .base_api import BaseAPI
from config.models import ANTHROPIC_MODELS

class AnthropicAPI(BaseAPI):
    def __init__(self):
        super().__init__()  # Initialize BaseAPI
        self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = ANTHROPIC_MODELS[0]
        
    async def send_message(self, message, tools=None):
        """Send a message to the Anthropic API
        
        Args:
            message: The user message
            tools: Optional list of available tools
        """
        try:
            messages = [{"role": "user", "content": message}]
            
            # If tools were used, append their results to the message
            if isinstance(message, str) and "Tool results:" in message:
                messages = [{"role": "user", "content": message}]
            
            stream = await self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=messages,
                stream=True
            )
            
            # Handle streaming response
            async for chunk in stream:
                if chunk.type == "content_block_delta":
                    yield chunk.delta.text
        except Exception as e:
            yield f"Anthropic API Error: {str(e)}"
            
    def get_name(self):
        return "anthropic"
        
    def get_available_models(self):
        return ANTHROPIC_MODELS
        
    def set_model(self, model_name):
        if model_name in ANTHROPIC_MODELS:
            self.model = model_name
            return True
        return False
