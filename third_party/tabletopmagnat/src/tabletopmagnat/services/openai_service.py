from copy import deepcopy
from typing import Any

from langfuse.openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletion,
)

from openai._types import Omit

from tabletopmagnat.config.openai_config import OpenAIConfig
from tabletopmagnat.types.dialog import Dialog
from tabletopmagnat.types.messages import AiMessage
from tabletopmagnat.types.messages.tool_message import ToolMessage
from tabletopmagnat.types.tool.openai_tool_params import OpenAIToolParams


class OpenAIService:
    def __init__(self, model_name: str, model_config: OpenAIConfig) -> None:
        self.tools: list[OpenAIToolParams] = []
        self.config = model_config
        self.model: str = model_name
        self.client = AsyncOpenAI(
            api_key=model_config.api_key,
            base_url=model_config.base_url,
        )
        self.structure = None

    def __deepcopy__(self, memo: dict[int, object] | None = None) -> object:
        new_instance = self.__class__(self.model, self.config)
        memo[id(self)] = new_instance
        return new_instance

    def add_mcp_tool(self, tool: OpenAIToolParams) -> None:
        if tool not in self.tools:
            self.tools.append(tool)

    def add_mcp_tools(self, tools: list[OpenAIToolParams]) -> None:
        tmp_tools = [tool for tool in tools if tool not in self.tools]
        self.tools.extend(tmp_tools)

    def bind_structured(self, structure: Any) -> None:
        self.structure = structure

    async def generate(self, dialog: Dialog) -> AiMessage:
        openai_tools = [tool.model_dump(by_alias=True) for tool in self.tools]

        response: ChatCompletion | None = None
        metadata = None
        content = ""

        if self.structure:
            response = await self.client.chat.completions.parse(
                messages=dialog.to_list(),
                model=self.model,
                response_format=self.structure,
            )
            metadata = response.choices[0].message.parsed
            metadata = metadata.model_dump() if metadata else None
        else:
            response: ChatCompletion = await self.client.chat.completions.create(
                messages=dialog.to_list(),
                model=self.model,
                tools=Omit() if not openai_tools else openai_tools,
            )

            content = response.choices[0].message.content
            content = "" if content is None else content.strip()

        tools_openai = response.choices[0].message.tool_calls
        tools = (
            [
                ToolMessage(
                    name=tool.function.name,
                    tool_call_id=tool.id,
                    content=tool.function.arguments,
                )
                for tool in tools_openai
            ]
            if tools_openai
            else []
        )

        # TODO: How will be better to handle this?
        response_msg = AiMessage(
            content=content,
            tool_calls=tools_openai,
            internal_tools=tools,
            metadata=metadata,
        )

        return response_msg
