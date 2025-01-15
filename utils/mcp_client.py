import json
import asyncio
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self):
        config_path = Path(__file__).parent.parent / "config" / "blnk_mcp_config.json"
        with open(config_path) as f:
            self.config = json.load(f)
            
        self.server_params = StdioServerParameters(
            command=self.config["server"]["command"],
            args=self.config["server"]["args"],
            env=self.config["server"]["env"]
        )
        self.tools = []
        self.session = None
        self.read = None
        self.write = None
        
    async def connect(self):
        """Establish connection to MCP server"""
        try:
            self.read, self.write = await stdio_client(self.server_params).__aenter__()
            self.session = await ClientSession(self.read, self.write).__aenter__()
            await self.session.initialize()
        except FileNotFoundError as e:
            print(f"Error: Could not start MCP server - {str(e)}")
            print("Please check that Python and mcp_server.py are available")
            return False
        except Exception as e:
            print(f"Error connecting to MCP server: {str(e)}")
            return False
        return True
        
    async def disconnect(self):
        """Clean up MCP connection"""
        if self.session:
            await self.session.__aexit__(None, None, None)
        if self.read and self.write:
            await stdio_client(self.server_params).__aexit__(None, None, None)
            
    async def refresh_tools(self):
        """Get latest available tools from server"""
        if not self.session:
            await self.connect()
        self.tools = await self.session.list_tools()
        return self.tools
        
    async def execute_tool(self, tool_name, tool_input):
        """Execute a tool with given input"""
        if not self.session:
            await self.connect()
        try:
            result = await self.session.call_tool(tool_name, tool_input)
            return result
        except Exception as e:
            return f"Tool execution failed: {str(e)}"
            
    def get_available_tools(self):
        """Return list of available tools"""
        return self.tools

    async def __aenter__(self):
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
