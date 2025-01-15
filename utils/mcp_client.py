import json
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
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
        self._client = None
        self._session = None
        
    @asynccontextmanager
    async def get_session(self):
        """Get a session context manager"""
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                yield session
                
    async def connect(self):
        """Establish connection to MCP server"""
        try:
            async with self.get_session() as session:
                await session.initialize()
                tools_response = await session.list_tools()
                self.tools = tools_response.tools if hasattr(tools_response, 'tools') else []
                return True
        except FileNotFoundError as e:
            print(f"Error: Could not start MCP server - {str(e)}")
            print("Please check that Node.js and the MCP server are available")
            return False
        except Exception as e:
            print(f"Error connecting to MCP server: {str(e)}")
            return False
        
    async def refresh_tools(self):
        """Get latest available tools from server"""
        async with self.get_session() as session:
            self.tools = await session.list_tools()
            return self.tools
        
    async def run_tool(self, tool_name, tool_input):
        """Execute a tool with given input while maintaining session"""
        try:
            async with self.get_session() as session:
                await session.initialize()  # Ensure session is initialized
                result = await session.call_tool(tool_name, tool_input)
                return result
        except Exception as e:
            return f"Tool execution failed: {str(e)}"
            
    def get_available_tools(self):
        """Return list of available tools"""
        return self.tools
