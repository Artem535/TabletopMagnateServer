from dataclasses import dataclass
from tabletopmagnat.pocketflow import AsyncFlow


@dataclass(slots=True)
class ExpertState:
    expert_1: AsyncFlow
    expert_2: AsyncFlow
    expert_3: AsyncFlow

    def to_list(self):
        return [self.expert_1, self.expert_2, self.expert_3]
