import json
import os
from pathlib import Path

class ConfigLoader:
    @staticmethod
    def load_config():
        config_path = Path(__file__).parent.parent / "config" / "config.json"
        
        # Create default config if it doesn't exist
        if not config_path.exists():
            default_config = {
                "default_api": "openai",
                "default_models": {
                    "openai": "gpt-4o",
                    "anthropic": "claude-3-5-sonnet-20241022",
                    "gemini": "gemini-2.0-flash-exp"
                },
                "max_tokens": {
                    "openai": 2000,
                    "anthropic": 1000,
                    "gemini": 1000
                }
            }
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
            
        # Load existing config
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return None
