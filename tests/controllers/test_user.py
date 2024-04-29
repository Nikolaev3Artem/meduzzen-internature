from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db.alchemy.models import User
from tests.constants import (
    test_user_create_email,
    test_user_create_username,
    updated_username,
    user_bad_id,
    user_create,
    users,
)


def test_user_get_list(client: TestClient, prepare_database, fill_database):
    response = client.get("/user/?limit=4&offset=0")
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 4
    for index, user in enumerate(users):
        assert response_data[index]["username"] == user["username"]
        assert response_data[index]["email"] == user["email"]


def test_user_create(client: TestClient, prepare_database, fill_database):
    response = client.post(
        "/user/",
        json={
            "email": user_create.email,
            "username": user_create.username,
            "password": user_create.password,
        },
    )
    result_data = response.json()
    assert response.status_code == 201
    assert result_data["email"] == test_user_create_email
    assert result_data["username"] == test_user_create_username


def test_user_get(client: TestClient, prepare_database, fill_database):
    test_user = client.get("/user/?limit=1&offset=0")
    test_user_id = test_user.json()[0]["id"]
    response = client.get(f"/user/{test_user_id}")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["email"] == users[0]["email"]
    assert response_data["username"] == users[0]["username"]


def test_user_not_found_error(client: TestClient, prepare_database, fill_database):
    response = client.get(f"/user/{user_bad_id}")
    assert response.status_code == 404


async def test_user_update(
    client: TestClient, prepare_database, fill_database, user_tests_token, session
):
    test_user = await session.execute(select(User).limit(1).offset(1))
    test_user_id = test_user.scalar().id
    response = client.patch(
        f"/user/{test_user_id}",
        json={
            "username": updated_username,
        },
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == updated_username


async def test_user_delete(
    client: TestClient, prepare_database, fill_database, user_tests_token, session
):
    test_user = await session.execute(select(User).limit(1).offset(1))
    test_user_id = test_user.scalar().id
    response = client.patch(
        f"/user/{test_user_id}/deactivate",
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )
    assert response.status_code == 204
