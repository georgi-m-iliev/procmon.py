import psutil
import asyncio
from collections import deque
from typing import Literal, Annotated

from app.models import SharedState, Process
from app.core.config import settings


async def background_worker(state: SharedState):
    cpu_count = psutil.cpu_count(logical=True)

    while True:
        processes_list = []

        processes = {p.pid: p for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])}
        for proc in processes.values():
            try:
                proc.cpu_percent(interval=None)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        await asyncio.sleep(5)

        for pid, proc in processes.items():
            try:
                with proc.oneshot():
                    process = Process(
                        pid=proc.pid,
                        name=proc.name(),
                        cpu_usage=proc.cpu_percent(interval=0) / cpu_count,
                        memory_usage=proc.memory_percent(),
                    )
                    processes_list.append(process)
                    key = (process.pid, process.name)
                    if key not in state.history:
                        state.history[key] = {
                            'cpu': deque(maxlen=settings.ROLLING_WINDOW_SIZE),
                            'mem': deque(maxlen=settings.ROLLING_WINDOW_SIZE),
                        }
                    state.history[key]['cpu'].append(process.cpu_usage)
                    state.history[key]['mem'].append(process.memory_usage)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        state.processes = processes_list
