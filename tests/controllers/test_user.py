from fastapi.testclient import TestClient

from tests.constants import user


def test_user_create(client: TestClient):
    response = client.post(
        "/user/",
        json=user,
    )
    assert response.status_code == 200


# def test_user_duplicated_keys(client: TestClient):
#     response = client.post(
#         "/user/",
#         json=user,
#     )
#     assert response.status_code == 409


def test_user_get_list(client: TestClient):
    response = client.get("/user/")
    assert response.status_code == 200


def test_user_get(client: TestClient):
    test_user = client.get("/user/")
    test_user_id = test_user.json()[0][0]["id"]
    response = client.get(f"/user/?user_id={test_user_id}")
    assert response.status_code == 200


def test_user_update(client: TestClient):
    test_user = client.get("/user/")
    test_user_id = test_user.json()[0][0]["id"]
    response = client.patch(
        f"/user/?user_id={test_user_id}",
        json={
            "username": "updated_username",
        },
    )
    assert response.status_code == 200


def test_user_delete(client: TestClient):
    test_user = client.get("/user/")
    test_user_id = test_user.json()[0][0]["id"]
    response = client.delete(f"/user/?user_id={test_user_id}")
    assert response.status_code == 200
