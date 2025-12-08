from typing import override

from langfuse import observe

from tabletopmagnat.node.abstract_parallel_node import AbstractParallelNode
from tabletopmagnat.pocketflow import AsyncFlow
from tabletopmagnat.state.expert_state import ExpertState
from tabletopmagnat.state.private_state import PrivateState


class ExpertParallelCoordinator(AbstractParallelNode):
    def __init__(
        self,
        name,
        expert_state: ExpertState,
        max_retries=3,
        wait: int | float = 1,
    ):
        super().__init__(name, max_retries, wait)
        self._expert_state = expert_state

    @observe(as_type="chain")
    @override
    async def prep_async(
        self, shared: PrivateState
    ) -> list[tuple[AsyncFlow, PrivateState]]:
        res = [(expert, shared) for expert in self._expert_state.to_list()]
        return res

    @observe(as_type="chain")
    @override
    async def exec_async(self, prep_res: tuple[AsyncFlow, PrivateState]) -> None:
        flow, shared = prep_res
        await flow.run_async(shared)

    @observe(as_type="chain")
    @override
    async def post_async(
        self,
        shared: PrivateState,
        prep_res: tuple[AsyncFlow, PrivateState],
        exec_res: None,
    ) -> str:
        return "default"
