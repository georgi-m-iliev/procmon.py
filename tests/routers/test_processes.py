from unittest import mock

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings, Settings
from app.models import ProcessList, Process
from app.dependencies import get_processes_from_shared_state


@pytest.fixture
def mock_settings():
    """Mock the settings object"""
    mock_settings = mock.Mock(Settings)
    mock_settings.PROJECT_NAME = "Test Project"
    mock_settings.PROJECT_VERSION = ""
    mock_settings.PROCESS_REFRESH_INTERVAL = 3
    return mock_settings


processes_example = [
        Process(pid=1, name="WindowsLogonService", cpu_usage=0.5, memory_usage=10),
        Process(pid=2, name="WindowsAnotherService", cpu_usage=0.2, memory_usage=50),
        Process(pid=3, name="Virus", cpu_usage=0.2, memory_usage=4),
    ]


async def mock_get_processes_from_shared_state(request: Request) -> list[Process]:
    return processes_example


@mock.patch("app.core.config.settings", new=mock_settings)
async def test_get_processes(mock_settings):
    app.dependency_overrides[get_processes_from_shared_state] = mock_get_processes_from_shared_state
    app.dependency_overrides[Settings] = mock_settings

    client = TestClient(app)
    response = await client.get("/processes")

    assert response.status_code == 200
    assert response.json() == {
        "processes": processes_example,
        "columns": ["pid", "name", "cpu_usage", "memory_usage"],
        "size": 3
    }
