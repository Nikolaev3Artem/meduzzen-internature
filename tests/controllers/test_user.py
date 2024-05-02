from fastapi.testclient import TestClient

from tests.constants import (
    test_user_create_email,
    test_user_create_username,
    updated_username,
    user_bad_id,
    user_create,
    users_list,
)


def test_user_get_list(client: TestClient, users):
    response = client.get("/user/?limit=4&offset=0")
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 4
    for index, user in enumerate(response_data):
        assert user["username"] == users_list[index]["username"]
        assert user["email"] == users_list[index]["email"]


def test_user_create(client: TestClient, users):
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


def test_user_get(client: TestClient, users):
    response = client.get(f"/user/{users[0].id}")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["email"] == users_list[0]["email"]
    assert response_data["username"] == users_list[0]["username"]


def test_user_not_found_error(client: TestClient, users):
    response = client.get(f"/user/{user_bad_id}")
    assert response.status_code == 404


async def test_user_update(client: TestClient, users, user_tests_token):
    response = client.patch(
        f"/user/{users[1].id}",
        json={
            "username": updated_username,
        },
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == updated_username


async def test_user_delete(client: TestClient, users, user_tests_token):
    response = client.patch(
        f"/user/{users[1].id}/deactivate",
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )
    assert response.status_code == 204
