from pydantic import BaseModel, Field

class FunctionParams(BaseModel):
    name: str
    description: str
    parameters: dict

class OpenAIToolParams(BaseModel):
    fn_type: str = Field(default="function", alias="type")
    fn_params: FunctionParams = Field(alias="function")

