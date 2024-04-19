from fastapi.testclient import TestClient

from tests.constants import user, user_bad_id


def test_user_create(client: TestClient):
    response = client.post(
        "/user/",
        json={
            "email": user.email,
            "username": user.username,
            "password": user.password,
        },
    )
    result_data = response.json()
    assert response.status_code == 200
    assert result_data["email"] == user.email
    assert result_data["username"] == user.username


def test_user_get_list(client: TestClient):
    response = client.get("/user/")
    assert response.status_code == 200


def test_user_get(client: TestClient):
    test_user = client.get("/user/")
    test_user_id = test_user.json()[0][0]["id"]
    response = client.get(f"/user/{test_user_id}")
    assert response.status_code == 200


def test_user_not_found_error(client: TestClient):
    response = client.get(f"/user/{user_bad_id}")
    assert response.status_code == 404


def test_user_update(client: TestClient):
    test_user = client.get("/user/")
    test_user_id = test_user.json()[0][0]["id"]
    response = client.patch(
        f"/user/{test_user_id}",
        json={
            "username": "updated_username",
        },
    )
    assert response.status_code == 200


def test_user_delete(client: TestClient):
    test_user = client.get("/user/")
    test_user_id = test_user.json()[0][0]["id"]
    response = client.delete(f"/user/{test_user_id}")
    assert response.status_code == 200
