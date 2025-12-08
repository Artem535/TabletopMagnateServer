from pydantic import BaseModel,Field

class TaskSplitterOutput(BaseModel):
    task_for_expert1: str = Field(..., description="Task for expert 1")
    task_for_expert2: str = Field(..., description="Task for expert 2")
    task_for_expert3: str = Field(..., description="Task for expert 3")