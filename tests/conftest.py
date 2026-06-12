import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module

# Snapshot the initial in-memory activities so tests can reset state
_initial_activities = copy.deepcopy(app_module.activities)

@pytest.fixture
def client():
    with TestClient(app_module.app) as client:
        yield client

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: restore activities to the initial snapshot before each test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_initial_activities))
    yield
