import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.cliente_service import _cliente


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def limpar_banco():
    _cliente.clear()
    yield
    _cliente.clear()
