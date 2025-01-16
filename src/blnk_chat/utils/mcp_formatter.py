import json
import time
import asyncio
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live

console = Console()

class MCPFormatter:
    @staticmethod
    def format_thought(thought_json):
        """Format a single thought from MCP reasoner"""
        try:
            data = json.loads(thought_json) if isinstance(thought_json, str) else thought_json
            thought = data.get("thought", "")
            thought_num = data.get("thoughtNumber", 0)
            total_thoughts = data.get("totalThoughts", 0)
            
            # Format as markdown
            md = f"""
### Thought {thought_num}/{total_thoughts}

{thought}
"""
            return Markdown(md)
        except Exception as e:
            return f"Error formatting thought: {str(e)}"
            
    @staticmethod
    async def stream_thoughts(thoughts, delay=0.5):
        """Stream thoughts with a typing effect"""
        with Live(console=console, refresh_per_second=20) as live:
            for i, char in enumerate(thoughts):
                live.update(Markdown(thoughts[:i+1]))
                await asyncio.sleep(0.02)  # Adjust for typing speed
                
    @staticmethod
    def show_thinking():
        """Display thinking animation"""
        return Spinner("dots", text="Thinking...")
