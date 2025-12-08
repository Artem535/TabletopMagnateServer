"""

"""
from chonkie import MarkdownChef, MarkdownDocument

from tabletopmagnat.node.abstract_node import AbstractNode


class ChonkieNode(AbstractNode):
    def __init__(self, name: str, max_retries=10, wait: int | float = 10):
        super().__init__(name, max_retries, wait)
        self._chef: MarkdownChef = MarkdownChef()

    async def prep_async(self, shared):
        doc = shared["document"]
        return doc

    async def exec_async(self, prep_res):
        document = self._chef.parse(prep_res)
        return document

    async def post_async(self, shared, prep_res, exec_res):
        document: MarkdownDocument = exec_res
        original_document = shared["document"]

        for chunk in document.chunks:
            chunk.text = original_document["title"]

        shared["chunks"] = exec_res
        return "default"
