from typing import Literal, override

from langfuse import observe

from tabletopmagnat.state.private_state import PrivateState
from tabletopmagnat.types.dialog import Dialog
from tabletopmagnat.types.messages import UserMessage
from tabletopmagnat.node.abstract_node import AbstractNode

class JoinNode(AbstractNode):
    @observe(as_type="chain")
    @override
    async def prep_async(self, shared: PrivateState) -> list[Dialog]:
        experts_dialog = [shared.expert_1, shared.expert_2, shared.expert_3]

        return experts_dialog

    @observe(as_type="chain")
    @override
    async def exec_async(self, prep_res: list[Dialog]) -> str:
        experts_dialog = prep_res
        experts_dialog = [
            dialog.get_last_message().content for dialog in experts_dialog
        ]
        result = "\n---\n".join(experts_dialog)

        return result

    @observe(as_type="chain")
    @override
    async def post_async(
        self,
        shared: PrivateState,
        prep_res: list[Dialog],
        exec_res: str,
    ) -> Literal["default"]:
        summery: Dialog = shared.summary
        message = f"Create a summary of the following rulebook created by experts:\n{exec_res}"
        summery.add_message(UserMessage(content=message))
        return "default"
