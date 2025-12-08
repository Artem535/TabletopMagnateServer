from typing import override

from tabletopmagnat.node.abstract_node import AbstractNode
from tabletopmagnat.state.private_state import PrivateState
from tabletopmagnat.types.dialog import Dialog
from tabletopmagnat.types.messages import AiMessage


class EchoNode(AbstractNode):
    def __init__(self, name: str, echo_text: str, max_retries=10, wait: int | float = 10):
        super().__init__(name, max_retries, wait)
        self._echo_text = echo_text

    async def prep_async(self, shared: PrivateState):
        return None

    async def exec_async(self, prep_res):
        return AiMessage(content=self._echo_text)

    async def post_async(self, shared: PrivateState, prep_res, exec_res):
        shared.dialog.add_message(exec_res)
        return "default"
