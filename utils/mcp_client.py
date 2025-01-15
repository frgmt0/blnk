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
        
    async def initialize(self):
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                self.tools = await session.list_tools()
                return self.tools
                
    async def call_tool(self, tool_name, tool_input):
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, tool_input)
                return result
