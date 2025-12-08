from typing import override

from tabletopmagnat.node.abstract_node import AbstractNode
from tabletopmagnat.state.private_state import PrivateState
from tabletopmagnat.types.dialog import Dialog
from tabletopmagnat.types.messages import AiMessage


class FromSummaryToMain(AbstractNode):
    @override
    async def prep_async(self, shared: PrivateState):
        return shared.summary

    @override
    async def exec_async(self,prep_res: Dialog):
        last_msg = prep_res.get_last_message()
        return last_msg

    @override
    async def post_async(self,shared: PrivateState,prep_res:Dialog,exec_res:AiMessage):
        shared.dialog.add_message(exec_res)
        return "default"