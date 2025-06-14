import pytest
from app import PyShellApp


@pytest.fixture
def app():
    return PyShellApp()

@pytest.fixture
def test_client(app):
    return app.test_session({})