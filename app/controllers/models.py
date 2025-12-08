from blacksheep import Response
from blacksheep.server.controllers import APIController, get, Controller, abstract

from domain.models.llm_models import LLMModels
from domain.models.openai import ModelListResponse, ModelInfo


class Models(APIController):
    @classmethod
    def version(cls) -> str | None:
        return "v1"

    @get()
    async def get_models(self) -> ModelListResponse:
        """Get the list of the supported models."""
        return ModelListResponse(
            data=[
                ModelInfo(id=str(LLMModels.MODEL_NAME.value), owned_by="raft"),
            ]
        )
