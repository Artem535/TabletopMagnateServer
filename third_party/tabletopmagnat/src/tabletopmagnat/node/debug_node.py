from icecream import ic
from pocketflow import AsyncNode


class DebugNode(AsyncNode):
    async def prep_async(self, shared):
        ic("DebugNode:prep_async|", shared)
        return shared

    async def run_async(self, shared):
        ic("DebugNode:run_async|", shared)
        return None

    async def post_async(self, shared, prep_res, exec_res):
        ic("DebugNode:post_async|", shared, prep_res, exec_res)
        return "default"
