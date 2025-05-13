import copy
import psutil

from fastapi import Request

from app.models import Process


async def get_processes_from_shared_state(request: Request) -> list[Process]:
    async with request.app.state.shared_state_lock:
        return copy.deepcopy(request.app.state.shared_state.processes)


async def get_history_from_shared_state(request: Request) -> dict:
    async with request.app.state.shared_state_lock:
        return copy.deepcopy(request.app.state.shared_state.history)
