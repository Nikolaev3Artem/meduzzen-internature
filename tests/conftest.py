from fastapi.testclient import TestClient
from app.main import app
from pytest import fixture

@fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()