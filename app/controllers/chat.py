from blacksheep import HTTPException
from blacksheep.server.controllers import APIController, get, Controller, abstract, post
from domain.service.llm_service import LLMService
from tabletopmagnat.types.dialog.dialog import Dialog
from domain.models.openai import ChatCompletionRequest, ChatCompletionResponse


class Chat(APIController):
    llm_service: LLMService

    @classmethod
    def version(cls) -> str | None:
        return "v1"

    @post("/completions")
    async def post_completions(
        self, req: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        """Create a completion by using llm_service."""
        if req.stream:
            raise HTTPException(status=501, message="Streaming is not implemented yet")

        response = await self.llm_service.run(req)
        return response
