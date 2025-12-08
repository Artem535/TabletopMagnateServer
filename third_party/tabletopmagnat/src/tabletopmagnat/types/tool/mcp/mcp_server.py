from typing import Literal

from pydantic import BaseModel

from tabletopmagnat.types.tool import ToolHeader


class MCPServer(BaseModel):
    transport: Literal["http", "sse"]
    url: str
    headers: ToolHeader
    auth: Literal["oauth", "bearer"]
