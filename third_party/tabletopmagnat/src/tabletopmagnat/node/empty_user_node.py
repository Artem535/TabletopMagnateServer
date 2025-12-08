from pocketflow import AsyncNode
from tabletopmagnat.types.dialog import Dialog

from tabletopmagnat.types.messages import UserMessage


class EmptyUserNode(AsyncNode):
    async def exec_async(self, prep_res):
        return UserMessage(content="")

    async def post_async(self, shared, prep_res, exec_res):
        dialog: Dialog = shared["dialog"]
        dialog.add_message(exec_res)
        return "default"
