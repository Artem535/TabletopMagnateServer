from abc import ABC

from langfuse import get_client
from tabletopmagnat.pocketflow import AsyncNode


class AbstractNode(AsyncNode, ABC):
    def __init__(self, name: str, max_retries=3, wait: int | float = 1):
        super().__init__(max_retries=max_retries, wait=wait)
        self._name = name
        self._lf_client = get_client()
