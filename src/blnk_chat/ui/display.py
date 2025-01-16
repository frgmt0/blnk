from pathlib import Path
from .colors import Colors
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.theme import Theme

class Display:
    def __init__(self):
        # Create custom theme that matches your color scheme
        theme = Theme({
            "info": "cyan",
            "warning": "yellow",
            "error": "red",
            "success": "green"
        })
        self.console = Console(theme=theme)
        self.config_path = Path(__file__).parent.parent / "config" / "config.json"

    def show_welcome(self):
        # Check if setup is completed
        setup_completed = self.config_path.exists()
        
        if setup_completed:
            welcome_md = f"""
blnk is ready to chat! Type `/help` to see available commands.

Made with ♥ by frgmt0_o
"""
        else:
            welcome_md = f"""
blnk is a powerful terminal-based chat application that lets you seamlessly interact with multiple AI providers.

To get started, run:
```
/setup    # Configure your API providers and settings
/help     # View all available commands
```

Made with ♥ by frgmt0_o
"""
        welcome_panel = Panel(
            Markdown(welcome_md),
            border_style="cyan",
            title="blnk",
            subtitle="v0.1.0"
        )
        self.console.print(welcome_panel)

    async def show_response(self, response, stream=False):
        """Show response with optional streaming"""
        try:
            if isinstance(response, str):
                md = Markdown(response)
                self.console.print(md)
            else:
                # Handle streaming response
                with self.console.status("[cyan]Thinking...", spinner="dots"):
                    current_text = ""
                    async for chunk in response:
                        if chunk:
                            current_text += chunk
                            self.console.clear()
                            self.console.print(Markdown(current_text))
        except Exception as e:
            # Fallback to plain text
            self.console.print(Panel(str(response), border_style="cyan"))
            
    def show_thinking(self):
        """Show thinking animation"""
        from ..utils.mcp_formatter import MCPFormatter
        return MCPFormatter.show_thinking()

    def show_error(self, error):
        self.console.print(Panel(f"Error: {error}", border_style="red"))

    def show_input_prompt(self):
        return self.console.input("[green]blnk>[/green] ")
