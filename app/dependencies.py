import psutil

from fastapi import Request

from app.models import SharedState


def get_shared_state(request: Request) -> SharedState:
    return request.app.state.shared_state
