from typing import Optional, Literal

from pydantic import BaseModel, computed_field


class Process(BaseModel):
    pid: int
    name: str
    cpu_usage: float
    memory_usage: float
    status: str


class ProcessList(BaseModel):
    processes: list[Process]

    @computed_field
    @property
    def size(self) -> int:
        return len(self.processes)


class SharedState:
    def __init__(self):
        self.processes = []
        self.history = {}
