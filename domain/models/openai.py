from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from domain.models.llm_models import LLMModels


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatCompletionRequest(BaseModel):
    model: LLMModels
    messages: List[Message]
    stream: bool = False
    max_tokens: Optional[int] = None
    temperature: Optional[float] = Field(0.7, ge=0, le=2)


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: Literal["stop", "length"]


class ChatCompletionResponse(BaseModel):
    id: str
    object: Literal["chat.completion"] = "chat.completion"
    model: str
    choices: List[Choice]


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
    owned_by: str


class ModelListResponse(BaseModel):
    object: str = "list"
    data: List[ModelInfo]
