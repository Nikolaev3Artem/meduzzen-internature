from fastapi.testclient import TestClient
from app.main import app
from pytest import fixture
client = TestClient(app)

@fixture(name="healthcheck")
def healthcheck():
    response = client.get("/")
    return response