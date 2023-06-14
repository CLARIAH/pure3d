import magic
import pytest
from src.app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client
