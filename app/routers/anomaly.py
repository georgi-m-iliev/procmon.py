from fastapi import APIRouter
from fastapi import Depends

from app.models import ProcessList, Process, SharedState
from app.core.config import settings
from app.dependencies import get_shared_state
from app.utils import rolling_stats, is_anomaly

router = APIRouter(prefix="/anomaly", tags=["anomaly"])


@router.get("/cpu", response_model=ProcessList)
async def get_memory_anomalies(state: SharedState = Depends(get_shared_state)):
    """
    Get a list of processes with memory anomalies.
    """
    anomalies = []
    for proc in state.processes:
        key = (proc.pid, proc.name)
        if key not in state.history:
            continue

        cpu_mean, cpu_std = rolling_stats(state.history[(proc.pid, proc.name)]['cpu'])
        if cpu_mean is None or cpu_std is None:
            continue

        if is_anomaly(proc.cpu_usage, cpu_mean, cpu_std, threshold=settings.ANOMALY_THRESHOLD):
            anomalies.append(proc)
    return ProcessList(processes=anomalies)


@router.get("/memory", response_model=ProcessList)
async def get_memory_anomalies(state: SharedState = Depends(get_shared_state)):
    """
    Get a list of processes with memory anomalies.
    """
    anomalies = []
    for proc in state.processes:
        key = (proc.pid, proc.name)
        if key not in state.history:
            continue

        mem_mean, mem_std = rolling_stats(state.history[(proc.pid, proc.name)]['mem'])
        if mem_mean is None or mem_std is None:
            continue

        if is_anomaly(proc.memory_usage, mem_mean, mem_std, threshold=settings.ANOMALY_THRESHOLD):
            anomalies.append(proc)
    return ProcessList(processes=anomalies)
