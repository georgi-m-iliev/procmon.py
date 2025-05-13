from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import processes, anomaly
from app.core.config import settings
from app.utils import lifespan


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(processes.router)
app.include_router(anomaly.router)
