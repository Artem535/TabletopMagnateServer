from pydantic import BaseModel, Field

from tabletopmagnat.types.tool.mcp.mcp_server import MCPServer


class MCPServers(BaseModel):
    mcp_server: dict[str, MCPServer] = Field(default_factory=dict, alias="mcpServers")
