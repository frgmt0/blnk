import os
import json
import yaml
from pathlib import Path
from rich.prompt import Prompt, Confirm
from rich.console import Console

class SetupManager:
    def __init__(self, config_path=None):
        # Use user's home directory for config
        self.config_dir = Path.home() / ".blnk" / "config"
        self.config_path = config_path or (self.config_dir / "config.json")
        self.valid_providers = ["anthropic", "openai", "gemini"]
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config = self._load_config()
        self.console = Console()

    def _load_config(self):
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {}

    def _save_config(self):
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Save config using absolute path
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def _save_keys(self, api_keys):
        """Save API keys to config.yaml"""
        try:
            config_dir = Path.home() / ".blnk" / "config"
            yaml_path = config_dir / "config.yaml"
            
            # Load existing config or use default
            if yaml_path.exists():
                with open(yaml_path) as f:
                    config = yaml.safe_load(f)
            else:
                config = {
                    'default_api': 'anthropic',
                    'default_models': {
                        'openai': 'gpt-4o',
                        'anthropic': 'claude-3-5-sonnet-20241022',
                        'gemini': 'gemini-2.0-flash-exp'
                    },
                    'api_keys': {}
                }
            
            # Update API keys
            if 'api_keys' not in config:
                config['api_keys'] = {}
            config['api_keys'].update(api_keys)

            # Save updated config
            with open(yaml_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
                    
            return True
        except Exception as e:
            print(f"\n[red]Error saving API keys: {str(e)}[/red]")
            return False

    def run_setup(self):
        print("\nWelcome to blnk setup!")
        
        # Get providers
        while True:
            providers_input = Prompt.ask(
                "\nWhich provider(s) would you like to set up? (comma-separated)",
                choices=self.valid_providers,
                show_choices=True
            )
            
            selected_providers = [p.strip().lower() for p in providers_input.split(',')]
            
            # Validate providers
            invalid_providers = [p for p in selected_providers if p not in self.valid_providers]
            if invalid_providers:
                print(f"\nInvalid provider(s): {', '.join(invalid_providers)}")
                print("Please try again with valid providers.")
                continue
            break

        # Collect API keys
        env_vars = {}
        for provider in selected_providers:
            while True:
                api_key = Prompt.ask(f"\nEnter your API Key: ({provider.title()})", password=True)
                if not api_key:
                    print("API key cannot be empty. Please try again.")
                    continue
                break
                
            env_key = f"{provider.upper()}_API_KEY"
            env_vars[env_key] = api_key

        # Save API keys to .env
        if self._save_keys(env_vars):
            self.console.print("\n[green]✓[/green] API keys successfully saved to .env file")
        else:
            self.console.print("\n[red]✗[/red] Failed to save API keys. Please check file permissions and try again.")
            return

        # Set default provider
        while True:
            default_provider = Prompt.ask(
                "\nWhich provider would you like to set as default?",
                choices=selected_providers,
                default=selected_providers[0]
            )
            if default_provider in selected_providers:
                break
            print(f"Please select from your configured providers: {', '.join(selected_providers)}")

        # Update config
        self.config["default_api"] = default_provider
        self.config["default_models"] = self.config.get("default_models", {})
        
        # Set default models for each provider
        from ..config.models import OPENAI_MODELS, ANTHROPIC_MODELS, GEMINI_MODELS
        model_maps = {
            "openai": OPENAI_MODELS,
            "anthropic": ANTHROPIC_MODELS,
            "gemini": GEMINI_MODELS
        }

        for provider in selected_providers:
            available_models = model_maps.get(provider, [])
            while True:
                print(f"\nAvailable models for {provider}:")
                for i, model in enumerate(available_models, 1):
                    print(f"{i}. {model}")
                    
                default_model = Prompt.ask(
                    f"\nSelect default model for {provider}",
                    choices=[str(i) for i in range(1, len(available_models) + 1)],
                    default="1"
                )
                
                try:
                    model_index = int(default_model) - 1
                    if 0 <= model_index < len(available_models):
                        self.config["default_models"][provider] = available_models[model_index]
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")

        # Save config
        try:
            self._save_config()
            self.console.print("\n[green]✓[/green] Configuration saved successfully!")
            self.console.print("\n[cyan]Setup complete![/cyan] You can now start using blnk.")
            self.console.print("\nTip: Use [green]/help[/green] to see available commands")
        except Exception as e:
            self.console.print(f"\n[red]✗[/red] Failed to save configuration: {str(e)}")
