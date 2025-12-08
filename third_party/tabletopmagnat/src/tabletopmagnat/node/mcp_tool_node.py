import json
from typing import Callable

from icecream import ic
from langfuse import observe

from tabletopmagnat.node.abstract_node import AbstractNode
from tabletopmagnat.state.private_state import PrivateState
from tabletopmagnat.types.dialog import Dialog
from tabletopmagnat.types.messages import AiMessage
from tabletopmagnat.types.messages.tool_message import ToolMessage
from tabletopmagnat.types.tool.mcp import MCPTools


class MCPToolNode(AbstractNode):
    def __init__(
        self,
        name: str,
        dialog_selector: Callable[[PrivateState], Dialog],
        mcp_tool: MCPTools,
        max_retires: int = 1,
        wait: float = 0,

    ):
        super().__init__(name, max_retires, wait)
        self._mcp_tool = mcp_tool
        self._dialog_selector = dialog_selector

    @observe(as_type="tool")
    async def prep_async(self, shared):
        name = f"{self._name}:prep"
        self._lf_client.update_current_span(name=name)

        dialog = self._dialog_selector(shared)
        last_msg: AiMessage = dialog.get_last_message()

        return last_msg.internal_tools or []

    @observe(as_type="tool")
    async def exec_async(self, prep_res):
        name = f"{self._name}:exec"
        self._lf_client.update_current_span(name=name)

        tool_calls: list[ToolMessage] = prep_res
        for tool_call in tool_calls:
            res = await self._mcp_tool.call_tool(tool_call.name, tool_call.content)
            tool_call.content = json.dumps(res.structured_content or "")
            ic("ToolNode:exec_async | tool result:", res)
        ic("ToolNode:exec_async | all tool calls:", tool_calls)
        return tool_calls

    @observe(as_type="tool")
    async def post_async(self, shared:PrivateState, prep_res, exec_res: list[ToolMessage]):
        name = f"{self._name}:post"
        self._lf_client.update_current_span(name=name)

        tool_calls: list[ToolMessage] = exec_res
        dialog = self._dialog_selector(shared)

        for tool_call in tool_calls:
            dialog.add_message(tool_call)

        return "default"
