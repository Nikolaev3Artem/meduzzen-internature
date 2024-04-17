import time

from httpx import AsyncClient


async def test_user_create(ac: AsyncClient):
    response = await ac.post(
        "/user/create/",
        json={
            "email": "testemail@gmail.com",
            "username": "test_username",
            "password": "test_password",
        },
    )
    time.sleep(15)
    assert response.status_code == 200


async def test_user_get(ac: AsyncClient):
    response = await ac.get("/user/")
    assert response.status_code == 200
    print(response.json())
