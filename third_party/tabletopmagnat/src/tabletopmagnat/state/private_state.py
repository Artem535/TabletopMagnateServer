from pydantic import BaseModel, Field

from tabletopmagnat.types.dialog import Dialog


class PrivateState(BaseModel):
    dialog: Dialog = Field(default_factory=Dialog)
    expert_1: Dialog = Field(default_factory=Dialog)
    expert_2: Dialog = Field(default_factory=Dialog)
    expert_3: Dialog = Field(default_factory=Dialog)
    summary: Dialog = Field(default_factory=Dialog)
