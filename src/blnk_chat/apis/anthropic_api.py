import os
import json
from anthropic import AsyncAnthropic
from .base_api import BaseAPI
from ..config.models import ANTHROPIC_MODELS
from ..utils.config_loader import ConfigLoader
from ..utils.token_tracker import TokenTracker

class AnthropicAPI(BaseAPI):
    def __init__(self):
        super().__init__()  # Initialize BaseAPI
        config = ConfigLoader.load_config()
        self.client = AsyncAnthropic(api_key=config['api_keys'].get('ANTHROPIC_API_KEY'))
        self.model = ANTHROPIC_MODELS[0]
        self.token_tracker = TokenTracker()
        
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

            # First count input tokens
            token_count = await self.client.messages.count_tokens(
                model=self.model,
                messages=messages,
                system=self.system_prompt + "\n\n" + self.style_prompt
            )
            input_tokens = token_count.token_count

            # Stream the response
            async with self.client.messages.stream(**request) as stream:
                # Track token usage and cache performance
                first_message = True
                total_text = ""
                async for text in stream.text_stream:
                    total_text += text
                    if first_message:
                        try:
                            # Get output token count from response metadata
                            output_tokens = stream.usage.output_tokens if hasattr(stream, 'usage') else 0
                            
                            # Get cache stats if available
                            usage = getattr(stream, 'usage', {}) or {}
                            if not isinstance(usage, dict):
                                usage = {}
                                
                            cache_created = usage.get('cache_creation_input_tokens', 0) 
                            cache_read = usage.get('cache_read_input_tokens', 0)
                            
                            # Calculate cache hit rate
                            total_input = input_tokens + cache_created + cache_read
                            cache_hit_rate = (cache_read / total_input * 100) if total_input > 0 else 0
                            
                            self.token_tracker.add_message(
                                input_tokens=input_tokens,
                                output_tokens=output_tokens,
                                cache_created=cache_created,
                                cache_read=cache_read,
                                cache_hit_rate=cache_hit_rate
                            )
                        except Exception as e:
                            print(f"Warning: Failed to track tokens: {str(e)}")
                        first_message = False
                
                    yield text
                
                # After message completion, yield token stats
                yield "\n" + self.token_tracker.format_stats()
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
