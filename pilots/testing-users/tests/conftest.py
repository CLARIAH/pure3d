import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    app.testing = True
    yield app.test_client()

