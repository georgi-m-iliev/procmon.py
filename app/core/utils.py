import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.models import SharedState
from app.procmon.background_task import background_worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    lock = asyncio.Lock()
    state = SharedState()
    app.state.shared_state_lock = lock
    app.state.shared_state = state
    asyncio.create_task(background_worker(state, lock))
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Background task cancelled.")
