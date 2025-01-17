import yaml
import json
from pathlib import Path

class ConfigLoader:
    @staticmethod
    def load_config():
        # Get config paths
        config_dir = Path.home() / ".blnk" / "config"
        yaml_path = config_dir / "config.yaml"
        json_path = config_dir / "config.json"
        
        config_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Load YAML config
            if yaml_path.exists():
                with open(yaml_path) as f:
                    config = yaml.safe_load(f)
                
                # Save as JSON for faster loading next time
                with open(json_path, 'w') as f:
                    json.dump(config, f, indent=4)
                
                return config
            
            # Fall back to JSON if it exists
            if json_path.exists():
                with open(json_path) as f:
                    return json.load(f)
                    
            # Return empty config with api_keys dict to avoid None errors
            return {
                "default_api": "anthropic",
                "api_keys": {},
                "default_models": {
                    "openai": "gpt-4o",
                    "anthropic": "claude-3-5-sonnet-20241022",
                    "gemini": "gemini-2.0-flash-exp"
                }
            }
            
        except Exception as e:
            print(f"Error loading config: {e}")
            return None
