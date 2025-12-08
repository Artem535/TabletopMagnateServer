from pydantic_settings import BaseSettings


class MCPSettings(BaseSettings):
    mcp_objectbox_url: str
