import pytest
from src.app import app
import magic


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()
