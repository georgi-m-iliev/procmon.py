from fastapi import APIRouter, Query, Depends
from typing import Annotated

from app.models import ProcessList, Process, FilterParams, SharedState
from app.core.config import settings
from app.dependencies import get_shared_state
from app.utils import rolling_stats, is_anomaly


router = APIRouter(prefix="/processes", tags=["processes"])


@router.get("", response_model=ProcessList)
async def get_processes(params: Annotated[FilterParams, Query()],
                        state: SharedState = Depends(get_shared_state)):
    """
    Get a list of processes with optional filtering and sorting.
    """

    if params.order_by:
        state.processes.sort(
            key=lambda x: getattr(x, str(params.order_by)),
            reverse=(params.order == "desc"))
    if params.limit:
        state.processes = state.processes[:params.limit]
    return ProcessList(processes=state.processes)


@router.get("/{process_name}", response_model=ProcessList)
async def get_processes_by_name(process_name: str,
                                params: Annotated[FilterParams, Query()],
                                state: SharedState = Depends(get_shared_state)):
    """
    Get a list of processes filtered by name.
    """

    if process_name:
        state.processes = [p for p in state.processes if process_name in p.name]
    if params.order_by:
        state.processes.sort(
            key=lambda x: getattr(x, str(params.order_by)),
            reverse=(params.order == "desc"))
    if params.limit:
        state.processes = state.processes[:params.limit]
    return ProcessList(processes=state.processes)
