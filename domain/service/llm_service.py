from tabletopmagnat.types.messages import UserMessage, AiMessage, SystemMessage

from app.settings import Settings
from tabletopmagnat.service.llm_service import Service
from tabletopmagnat.types.dialog.dialog import Dialog
from tabletopmagnat.types.messages.base_message import BaseMessage

from domain.exceptions import LLMProcessingError, AppBaseException
from domain.models.openai import ChatCompletionRequest


class LLMService:
    def __init__(self, settings: Settings):
        self.llm_service: Service = Service(settings.service)

    def convert_to_msg(self, content: str, role: str) -> BaseMessage:
        msg: BaseMessage | None = None

        if role == 'user':
            msg = UserMessage(content=content)
        elif role == 'assistant':
            msg = AiMessage(content=content)
        elif role == 'system':
            msg = SystemMessage(content=content)

        return msg

    async def run(self, req: ChatCompletionRequest) -> str:
        try:
            dialog = Dialog(messages=[self.convert_to_msg(msg.content, msg.role) for msg in req.messages])
            result = await self.llm_service.run(dialog)
        except AppBaseException as e:
            raise LLMProcessingError(str(e))

        return str(result)
