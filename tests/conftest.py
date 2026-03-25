import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

@pytest.fixture
def client():
    """Provide a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before and after each test."""
    original_state = copy.deepcopy(activities)
    
    yield
    
    activities.clear()
    activities.update(original_state)