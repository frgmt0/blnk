import json
import os
from pathlib import Path

class ConfigLoader:
    @staticmethod
    def load_config():
        # Create config directory in user's home
        config_dir = Path.home() / ".blnk" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_path = config_dir / "config.json"
        
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
                },
                "api_keys": {}
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
