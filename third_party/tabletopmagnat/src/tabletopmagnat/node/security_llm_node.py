from typing import override

from icecream import ic
from langfuse import observe

from tabletopmagnat.node.llm_node import LLMNode
from tabletopmagnat.state.private_state import PrivateState
from tabletopmagnat.types.dialog import Dialog
from tabletopmagnat.types.messages import SystemMessage, AiMessage


class SecurityNode(LLMNode):
    @override
    @observe(as_type="guardrail")
    def get_prompt(self) -> SystemMessage:
        name = f"{self._name}:get_prompt"
        self._lf_client.update_current_span(name=name)

        prompt = self._lf_client.get_prompt("security")
        return SystemMessage(content=prompt.prompt)

    @override
    @observe(name="TaskClassifier:post", as_type="chain")
    async def post_async(self, shared: PrivateState, prep_res, exec_res):
        """Handles post-processing after execution.

        Logs the AI response using `icecream`, adds the AI message to the dialog, and returns a status.

        Args:
            shared (dict[str, Any]): Shared context containing the dialog.
            prep_res (Dialog): The prepared dialog (not used here).
            exec_res (AiMessage): The AI-generated message from execution.

        Returns:
            str: A default return value ("default") indicating completion.
        """
        self._lf_client.update_current_span(name=f"{self._name}:post", metadata=exec_res.metadata)

        ic("TaskClassifier:post| exec_res:", exec_res)
        msg: AiMessage = exec_res

        assert "verdict" in msg.metadata, "No verdict in metadata"

        return msg.metadata["verdict"]