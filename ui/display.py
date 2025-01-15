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

    def show_welcome(self):
        welcome_md = f"""
# Welcome to blnk!

*A modular terminal chat application supporting multiple AI providers*

## Quick Start:
- Use `/apis` to see available AI providers
- Use `/use <api_name>` to select a provider
- Use `/model-list` to see available models
- Use `/switch-model <model_name>` to switch to a new model
- Start chatting!

Type `/help` for detailed command information
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
            if stream:
                from utils.mcp_formatter import MCPFormatter
                await MCPFormatter.stream_thoughts(response)
            else:
                md = Markdown(response)
                self.console.print(Panel(md, border_style="cyan"))
        except Exception:
            # Fallback to plain text
            self.console.print(Panel(response, border_style="cyan"))
            
    def show_thinking(self):
        """Show thinking animation"""
        from utils.mcp_formatter import MCPFormatter
        return MCPFormatter.show_thinking()

    def show_error(self, error):
        self.console.print(Panel(f"Error: {error}", border_style="red"))

    def show_input_prompt(self):
        return self.console.input("[green]blnk>[/green] ")
