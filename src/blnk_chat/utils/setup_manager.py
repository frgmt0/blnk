import os
import json
from pathlib import Path
from rich.prompt import Prompt, Confirm
from rich.console import Console

class SetupManager:
    def __init__(self, config_path=None, env_path=None):
        self.config_path = config_path or Path("config/config.json")
        self.env_path = env_path or Path(".env")
        self.valid_providers = ["anthropic", "openai", "gemini"]
        self.config = self._load_config()
        self.console = Console()

    def _load_config(self):
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {}

    def _save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def _save_env(self, env_vars):
        """Save environment variables to .env file with error handling"""
        try:
            # Ensure .env file exists
            self.env_path.touch(exist_ok=True)
            
            # Read existing env file
            existing_env = {}
            if self.env_path.stat().st_size > 0:
                with open(self.env_path) as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            existing_env[key] = value

            # Update with new values
            existing_env.update(env_vars)

            # Write back to file
            with open(self.env_path, 'w') as f:
                for key, value in existing_env.items():
                    f.write(f"{key}={value}\n")
                    
            return True
        except Exception as e:
            print(f"\n[red]Error saving environment variables: {str(e)}[/red]")
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
        if self._save_env(env_vars):
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
