from typing import override

from langfuse import observe

from tabletopmagnat.node.llm_node import LLMNode
from tabletopmagnat.types.messages import SystemMessage


class AssistantNode(LLMNode):

    @override
    @observe(as_type="chain")
    def get_prompt(self) -> SystemMessage:
        name = f"{self._name}:get_prompt"
        self._lf_client.update_current_span(name=name)

        prompt = self._lf_client.get_prompt("main")
        sys_msg = SystemMessage(content=prompt.prompt)
        return sys_msg
