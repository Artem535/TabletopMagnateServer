import uuid

from tabletopmagnat.services.llm_service import Service
from tabletopmagnat.types.dialog.dialog import Dialog
from tabletopmagnat.types.messages import AiMessage, SystemMessage, UserMessage
from tabletopmagnat.types.messages.base_message import BaseMessage

from app.settings import Settings
from domain.exceptions import AppBaseException, LLMProcessingError
from domain.models.openai import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    Choice,
    Message,
)


class LLMService:
    def __init__(self, settings: Settings):
        self.llm_service: Service = Service(settings.service)

    def convert_to_msg(self, content: str, role: str) -> BaseMessage:
        mapping = {
            "user": UserMessage,
            "assistant": AiMessage,
            "system": SystemMessage,
        }

        if role not in mapping:
            raise ValueError(f"Unknown role: {role}")

        res = mapping[role](content=content)
        return res

    async def run(self, req: ChatCompletionRequest) -> ChatCompletionResponse:
        try:
            dialog = Dialog(
                messages=[
                    self.convert_to_msg(msg.content, msg.role) for msg in req.messages
                ]
            )

            result: str = await self.llm_service.run(dialog)

            result = result.removeprefix("```")
            result = result.removeprefix("markdown")
            result = result.removesuffix("```")

        except AppBaseException as e:
            raise LLMProcessingError(e.message)

        completion_id = f"chatcmpl-{uuid.uuid4().hex}"
        chat_result = ChatCompletionResponse(
            id=completion_id,
            choices=[
                Choice(
                    index=0,
                    message=Message(role="assistant", content=result),
                    finish_reason="stop",
                )
            ],
            model=req.model.MODEL_NAME,
        )

        return chat_result
