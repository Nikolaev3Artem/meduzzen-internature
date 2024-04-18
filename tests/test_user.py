from httpx import AsyncClient
from .constants import user


def test_user_create(client: AsyncClient):
    response = client.post(
        "/user/create/",
        json=user,
    )
    assert response.status_code == 200


def test_user_get(client: AsyncClient):
    response = client.get("/user/")
    assert response.status_code == 200
