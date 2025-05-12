import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.models import SharedState
from app.core.config import settings
from app.core.background_task import background_worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    state = SharedState()
    app.state.shared_state = state
    asyncio.create_task(background_worker(state))
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Background task cancelled.")

