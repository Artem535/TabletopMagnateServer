import json

from fastmcp import Client
from fastmcp.client.client import CallToolResult

from tabletopmagnat.types.tool.mcp import MCPServers
from tabletopmagnat.types.tool.openai_tool_params import (
    FunctionParams,
    OpenAIToolParams,
)


class MCPTools:
    def __init__(self, mcp_servers: MCPServers):
        config = mcp_servers.model_dump(by_alias=True)
        self._client: Client = Client(config)
        self._tools_name: list[str | OpenAIToolParams] = []

    def get_client(self):
        return self._client

    async def get_tool_list(self):
        async with self._client:
            tools = await self._client.list_tools()
            self._tools_name = [tool.name for tool in tools]
            return tools

    async def get_openai_tools(self):
        async with self._client:
            tools = await self._client.list_tools()
            tools_json = [
                OpenAIToolParams(
                    function=FunctionParams(
                        name=tool.name,
                        description=tool.description,
                        parameters=tool.inputSchema,
                    )
                )
                for tool in tools
            ]

            self._tools_name = [tool.name for tool in tools]
            return tools_json

    async def call_tool(self, tool_name: str, tool_input: dict | str) -> CallToolResult:
        tools = json.loads(tool_input) if isinstance(tool_input, str) else tool_input

        async with self._client:
            if tool_name in self._tools_name:
                return await self._client.call_tool(tool_name, tools)

            raise ValueError(f"Tool {tool_name} not found")
