import os
import json
from anthropic import AsyncAnthropic
from .base_api import BaseAPI
from ..config.models import ANTHROPIC_MODELS
from ..utils.config_loader import ConfigLoader

class AnthropicAPI(BaseAPI):
    def __init__(self):
        super().__init__()  # Initialize BaseAPI
        config = ConfigLoader.load_config()
        self.client = AsyncAnthropic(api_key=config['api_keys'].get('ANTHROPIC_API_KEY'))
        self.model = ANTHROPIC_MODELS[0]
        
    async def send_message(self, message, tools=None):
        """Send a message to the Anthropic API with prompt caching
        
        Args:
            message: The user message
            tools: Optional list of available tools
        """
        try:
            # Build the request structure in the correct order for caching:
            # 1. Tools (if any)
            # 2. System messages
            # 3. Conversation messages
            
            request = {
                "model": self.model,
                "max_tokens": 1000,
                "messages": []
            }
            
            # 1. Add tools if provided
            if tools:
                request["tools"] = [{
                    "type": "text",
                    "text": json.dumps(tools),
                    "cache_control": {"type": "ephemeral"}
                }]
                
            # 2. Add system messages - these should be cached as they're stable
            system_content = [{
                "type": "text",
                "text": self.system_prompt + "\n\n" + self.style_prompt,
                "cache_control": {"type": "ephemeral"}  # Will be cached for 5 minutes
            }]
            
            # Only enable caching if the system prompt is long enough
            # (minimum 1024 tokens for Sonnet/Opus, 2048 for Haiku)
            if len(self.system_prompt + self.style_prompt) > 1024:  # Simple approximation
                request["system"] = system_content
                
            # 3. Add conversation messages
            messages = []
            
            # If there are tool results, add them as a separate message
            if isinstance(message, str) and "Tool results:" in message:
                parts = message.split("Tool results:")
                messages.extend([
                    {"role": "user", "content": parts[0].strip()},
                    {"role": "assistant", "content": "Let me process those tool results."},
                    {"role": "user", "content": f"Tool results: {parts[1].strip()}"}
                ])
            else:
                messages.append({"role": "user", "content": message})
                
            request["messages"] = messages

            # Stream the response
            async with self.client.messages.stream(**request) as stream:
                # Check cache performance from the first message
                first_message = True
                async for text in stream.text_stream:
                    if first_message and hasattr(stream, 'usage'):
                        # Log cache performance metrics
                        usage = stream.usage
                        cache_created = usage.get('cache_creation_input_tokens', 0)
                        cache_read = usage.get('cache_read_input_tokens', 0)
                        regular_input = usage.get('input_tokens', 0)
                        
                        if cache_created:
                            print(f"Created cache entry with {cache_created} tokens")
                        elif cache_read:
                            print(f"Read {cache_read} tokens from cache")
                        first_message = False
                    
                    yield text
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
