from typing import Literal

from pydantic import BaseModel, Field


class TaskClassifierOutput(BaseModel):
    task: Literal["web_search", "explanation", "clarification"] = Field(
        description="The task of the user. "
        "search -- search for tabletop information in the web. Used only if information is not found in the game rules. "
        "explanation -- explain the **FULL** rules of the tabletop game. Explanation will be from begin to end. "
        "clarification -- ask for clarification on the rules of the tabletop game. Answer will be contains the 1-2 sentence. "
    )
