from pydantic import BaseModel, Field

class ToolHeader(BaseModel):
    authorization: str = Field(default="empty_token", alias="Authorization")

    def set_auth(self, token: str):
        self.authorization = f"Bearer {token}"