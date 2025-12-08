from typing import override

from langfuse import observe

from tabletopmagnat.node.llm_node import LLMNode
from tabletopmagnat.state.private_state import PrivateState
from tabletopmagnat.types.messages import AiMessage, SystemMessage, UserMessage


class TaskSplitterNode(LLMNode):
    @override
    @observe(as_type="chain")
    def get_prompt(self) -> SystemMessage:
        name = f"{self._name}:get_prompt"
        self._lf_client.update_current_span(name=name)

        prompt = self._lf_client.get_prompt("task_splitter")
        return SystemMessage(content=prompt.prompt)


    def prepare_message(self, content: str) -> str:
        msg = f"Here is your task: {content}"
        msg += "\n---\n Always use tools to get information for task."
        return msg

    @override
    async def post_async(self, shared: PrivateState, prep_res, exec_res: AiMessage):
        assert "task_for_expert1" in exec_res.metadata, "No task for expert1 found"
        msg = self.prepare_message(exec_res.metadata["task_for_expert1"])
        shared.expert_1.add_message(UserMessage(content=msg))

        assert "task_for_expert2" in exec_res.metadata, "No task for expert2 found"
        msg = self.prepare_message(exec_res.metadata["task_for_expert2"])
        shared.expert_2.add_message(UserMessage(content=msg))

        assert "task_for_expert3" in exec_res.metadata, "No task for expert3 found"
        msg = self.prepare_message(exec_res.metadata["task_for_expert3"])
        shared.expert_3.add_message(UserMessage(content=msg))

        return "default"
