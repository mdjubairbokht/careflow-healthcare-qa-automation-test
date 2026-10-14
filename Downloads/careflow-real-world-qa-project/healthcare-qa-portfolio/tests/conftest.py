import pytest
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture
def client(tmp_path):
    """Isolated SQLite database per API test."""
    with TestClient(create_app(tmp_path / 'test.db')) as test_client:
        yield test_client
