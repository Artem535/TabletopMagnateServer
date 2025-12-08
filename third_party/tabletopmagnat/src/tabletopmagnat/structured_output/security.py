from typing import Literal

from pydantic import BaseModel, Field


class SecurityOutput(BaseModel):
    verdict: Literal["safe", "unsafe"] = Field(..., description="The verdict of the security check")
    user_input: str = Field(..., description="The user input that was checked")
    description: str = Field(..., description="The description of the security check")
