from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import processes, anomaly
from app.core.config import settings
from app.core.utils import lifespan

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

app.include_router(processes.router, prefix="/api")
app.include_router(anomaly.router, prefix="/api")

try:
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")


    @app.get("/")
    async def root():
        return FileResponse("frontend/dist/index.html")
except RuntimeError:
    print("Error mounting web ui files. Make sure the directory exists.")
