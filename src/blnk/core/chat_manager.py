import asyncio
import json
from ..apis.base_api import BaseAPI
from ..utils.mcp_client import MCPClient
                                                                                                            
class ChatManager:                                                                                             
    def __init__(self, config=None, display=None):                                                                                        
        self.apis = {}                                                                                         
        self.current_api = None
        self.config = config
        self.mcp_client = None
        self.display = display
        
    async def initialize_tools(self):
        """Initialize MCP client and load available tools"""
        self.mcp_client = MCPClient()
        await self.mcp_client.connect()
                                                                                                            
    def register_api(self, name, api_instance):                                                                
        if isinstance(api_instance, BaseAPI):                                                                  
            self.apis[name] = api_instance
            
            # Set default model if configured
            if self.config and name in self.config['default_models']:
                api_instance.set_model(self.config['default_models'][name])
                
            # Set as current API if it's the default
            if self.config and self.config['default_api'] == name:
                self.current_api = api_instance
                                                                                                            
    async def process_input(self, user_input):                                                                       
        if user_input.startswith('/'):                                                                         
            return self.handle_command(user_input[1:])                                                         
                                                                                                            
        if self.current_api:
            # Get available tools
            tools = self.mcp_client.get_available_tools() if self.mcp_client else []
            
            # First pass - send message with tools context
            full_response = ""
            async for chunk in self.current_api.send_message(
                f"Available tools: {tools}\n\nUser message: {user_input}"
            ):
                full_response += chunk
            
            # Check if response indicates tool use
            if "I would like to use the tool" in full_response:
                # Parse tool name and args from response
                # This is a simple example - you may want more robust parsing
                tool_name = full_response.split("use the tool")[1].split("with")[0].strip()
                tool_args = full_response.split("with arguments")[1].strip()
                
                # Show thinking animation while executing tool
                with self.display.show_thinking():
                    # Execute tool
                    tool_result = asyncio.run(self.mcp_client.run_tool(tool_name, tool_args))
                    
                    # Format MCP reasoner output if applicable
                    if tool_name == "mcp-reasoner":
                        from ..utils.mcp_formatter import MCPFormatter
                        formatted_result = MCPFormatter.format_thought(tool_result)
                        # Stream the formatted thoughts
                        await self.display.show_response(formatted_result, stream=True)
                    
                    # Send results back to model without showing to user
                    # Collect the full response
                    full_response = ""
                    async for chunk in self.current_api.send_message(
                        f"Tool results: {tool_result}\nContinue the conversation with the user."
                    ):
                        full_response += chunk
            return full_response
        return "No API selected. Use /api <name> to select an API."
                                                                                                            
    def handle_command(self, command):
        parts = command.split()
        cmd = parts[0].lower()

        if cmd == 'help':
            help_text = """
# Available Commands

## Basic Commands
- `/help` - Show this help message
- `/apis` - List available AI providers
- `/use <api>` - Switch to specified AI provider
- `/model-list` - Show available models for current/all providers
- `/switch-model` - Switch to a different model for current provider
- `/exit` - Exit the application
- `exit` - Exit the application (alternative)
- `/tools` - List available MCP tools and their descriptions

## Examples
```
/use openai             # Switch to OpenAI provider
/switch-model gpt-4o    # Switch to GPT-4 model
/tools                  # Show available tools
```
"""
            return help_text
        elif cmd == 'apis':
            return self.show_available_apis()
        elif cmd == 'model-list':
            return self.show_models()
        elif cmd == 'switch-model' and len(parts) > 1:
            return self.switch_model(' '.join(parts[1:]))
        elif cmd == 'use' and len(parts) > 1:
            api_name = parts[1].lower()
            if api_name in self.apis:
                self.current_api = self.apis[api_name]
                return f"Switched to {api_name} API"
            return f"API '{api_name}' not available. Use /apis to see available APIs."
        elif cmd == 'exit':
            raise KeyboardInterrupt
        elif cmd == 'tools':
            return self.show_available_tools()
        elif cmd == 'setup':
            from ..utils.setup_manager import SetupManager
            setup = SetupManager()
            setup.run_setup()
            return "Setup complete! Please restart blnk to apply changes."

        return f"Unknown command: {cmd}"

    def show_available_tools(self):
        """Display all available MCP tools"""
        if not self.mcp_client:
            return "# MCP client not initialized"
            
        tools = self.mcp_client.get_available_tools()
        if not tools:
            return "# No tools available"
            
        result = "# Available MCP Tools\n\n"
        for tool in tools:
            if isinstance(tool, tuple):
                name, details = tool
                result += f"## {name}\n"
                if isinstance(details, dict):
                    if 'description' in details:
                        result += f"*{details['description']}*\n\n"
                    if 'parameters' in details:
                        result += "### Parameters\n```json\n"
                        result += f"{json.dumps(details['parameters'], indent=2)}\n```\n"
            else:
                result += f"## {str(tool)}\n"
        return result

    def show_available_apis(self):
        if not self.apis:
            return "# No APIs configured\nPlease add API keys to your `.env` file."
        return "# Available APIs\n" + "\n".join(f"- {name}" for name in self.apis.keys())

    def show_models(self):
        if not self.apis:
            return "# No APIs available\nPlease add API keys to your `.env` file."
            
        if not self.current_api:
            result = "# Available models for all configured APIs\n"
            for api in self.apis.values():
                result += f"\n## {api.get_name().upper()}\n"
                result += "\n".join(f"- {model}" for model in api.get_available_models())
            return result
        
        models = self.current_api.get_available_models()
        return f"# Available models for {self.current_api.get_name()}\n" + "\n".join(f"- {model}" for model in models)
        
    def switch_model(self, model_name):
        if not self.current_api:
            return "No API selected. Please select an API first."
            
        if self.current_api.set_model(model_name):
            return f"Switched to model: {model_name}"
        return f"Invalid model name for {self.current_api.get_name()}"
