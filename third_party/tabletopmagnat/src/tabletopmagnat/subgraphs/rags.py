from copy import deepcopy
from typing import Callable

from blacksheep.server.controllers import abstract
from tabletopmagnat.node.abstract_node import AbstractNode
from tabletopmagnat.node.llm_node import LLMNode
from tabletopmagnat.node.mcp_tool_node import MCPToolNode
from tabletopmagnat.pocketflow import AsyncFlow, AsyncNode
from tabletopmagnat.services.openai_service import OpenAIService
from tabletopmagnat.types.dialog import Dialog
from tabletopmagnat.types.tool.mcp import MCPTools
from tabletopmagnat.types.tool.openai_tool_params import OpenAIToolParams
from tabletopmagnat.state.private_state import PrivateState


class RASG:
    @staticmethod
    async def create_subgraph(
        name: str,
        prompt_name: str,
        openai_service: OpenAIService,
        mcp_tools: MCPTools,
        dialog_selector: Callable[[PrivateState], Dialog],
    ):
        tools: list[OpenAIToolParams] = await mcp_tools.get_openai_tools()

        # Create universal node and bind tools to them
        universal_node = LLMNode(
            name=f"{name}_universal_node",
            prompt_name=prompt_name,
            dialog_selector=dialog_selector,
            llm_service=deepcopy(openai_service),
            max_retries=3,
            wait=2,
        )
        universal_node.bind_tools(tools)

        # Create tool nodes
        tool_node = MCPToolNode(
            name=f"{name}_tool_node",
            mcp_tool=mcp_tools,
            dialog_selector=dialog_selector,
        )

        abstract_node = AsyncNode()

        # Connect
        universal_node - "tools" >> tool_node
        universal_node - "default" >> abstract_node
        tool_node >> universal_node

        # Create flow
        flow = AsyncFlow(start=universal_node)

        return flow
