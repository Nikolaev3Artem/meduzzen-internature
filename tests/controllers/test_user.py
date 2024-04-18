from tests.constants import user
from fastapi.testclient import TestClient


def test_user_create(client: TestClient):
    response = client.post(
        "/user/create/",
        json=user,
    )
    assert response.status_code == 200


def test_user_get_list(client: TestClient):
    response = client.get("/user/")
    assert response.status_code == 200


def test_user_get(client: TestClient):
    response = client.get("/user/")
    assert response.status_code == 200
