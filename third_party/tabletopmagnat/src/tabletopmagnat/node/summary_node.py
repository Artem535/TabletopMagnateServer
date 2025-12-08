from langfuse import observe

from tabletopmagnat.node.abstract_node import AbstractNode
from tabletopmagnat.types.dialog import Dialog
from tabletopmagnat.types.messages import MessageRoles


class SummaryNode(AbstractNode):
    @observe(as_type="chain")
    async def prep_async(self, shared):
        name = f"{self._name}:prep"
        self._lf_client.update_current_span(name=name)

        dialog: Dialog = shared["dialog"]

        if len(dialog.messages) < 2:
            return shared

        last_msg = dialog.pop_last_message()
        if last_msg.role != MessageRoles.ASSISTANT:
            dialog.add_message(last_msg)
            return shared

        content_suffix = (
            f"\n\n<END_AGENT_TURN>\n\n---\n\n<ANSWER_DIFFERENT_AGENT>\n{last_msg.content}"
        )

        prev_msg = dialog.pop_last_message()
        if prev_msg.role != MessageRoles.USER:
            dialog.add_message(prev_msg)
            dialog.add_message(last_msg)
            raise RuntimeError(
                "SummaryNode: Broken dialog structure — expected USER before ASSISTANT"
            )

        prev_msg.content = (prev_msg.content or "") + content_suffix
        dialog.add_message(prev_msg)
        return shared
