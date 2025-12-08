from blacksheep.server.controllers import APIController, get, Controller, abstract, post
from domain.service.llm_service import LLMService
from tabletopmagnat.types.dialog.dialog import Dialog
from domain.models.openai import ChatCompletionRequest

class Chat(APIController):
    llm_service: LLMService

    @classmethod
    def version(cls) -> str | None:
        return "v1"

    @post("/completions")
    async def post_completions(self, req: ChatCompletionRequest) -> str:
        """Create a completion by using llm_service."""
        return await self.llm_service.run(req)
