import os
from anthropic import Anthropic
from .base_api import BaseAPI
from config.models import ANTHROPIC_MODELS

class AnthropicAPI(BaseAPI):
    def __init__(self):
        super().__init__()  # Initialize BaseAPI
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = ANTHROPIC_MODELS[0]
        
    def send_message(self, message):
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                tools=self.get_tool_config()
            )
            
            # Check if the response indicates tool use
            if hasattr(response, 'tool_calls') and response.tool_calls:
                return response
            return response.content[0].text
        except Exception as e:
            return f"Anthropic API Error: {str(e)}"
            
    def get_tool_config(self):
        """Get tool configuration for the API"""
        # Convert MCP tools to Anthropic format
        tools = []
        for tool in self.mcp_client.get_available_tools():
            if isinstance(tool, tuple):
                name, details = tool
                tool_config = {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": details.get("description", ""),
                        "parameters": details.get("parameters", {})
                    }
                }
                tools.append(tool_config)
        return tools
            
    def get_name(self):
        return "anthropic"
        
    def get_available_models(self):
        return ANTHROPIC_MODELS
        
    def set_model(self, model_name):
        if model_name in ANTHROPIC_MODELS:
            self.model = model_name
            return True
        return False
