from abc import ABC, abstractmethod
import asyncio
from utils.mcp_client import MCPClient

class BaseAPI(ABC):
    def __init__(self):
        self.mcp_client = MCPClient()
        self.available_tools = None
        
    async def initialize_tools(self):
        self.available_tools = await self.mcp_client.initialize()
        
    async def execute_tool(self, tool_name, tool_input):
        return await self.mcp_client.call_tool(tool_name, tool_input)

    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def get_name(self):
        pass
        
    @abstractmethod
    def get_available_models(self):
        pass
        
    @abstractmethod
    def set_model(self, model_name):
        pass
        
    def get_available_tools(self):
        return self.available_tools if self.available_tools else []
