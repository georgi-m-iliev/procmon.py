from fastapi import FastAPI

from app.routers import processes, anomaly
from app.core.config import settings
from app.utils import lifespan


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    lifespan=lifespan
)

app.include_router(processes.router)
app.include_router(anomaly.router)
