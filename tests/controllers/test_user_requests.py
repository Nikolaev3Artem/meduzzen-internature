from fastapi.testclient import TestClient

from tests.constants import test_user_leave


async def test_user_accept_invite(
    client: TestClient, company_requests, user_tests_token
):
    response = client.post(
        f"/user/{company_requests[1].id}/accept_invite",
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )

    assert response.status_code == 200


async def test_user_reject_invite(
    client: TestClient, company_requests, user_tests_token
):
    response = client.delete(
        f"/user/{company_requests[1].id}/reject_invite",
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )

    assert response.status_code == 204


async def test_user_send_join_request(client: TestClient, companies, user_tests_token):
    response = client.post(
        f"/user/{companies[1].id}/send_join_request",
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )

    assert response.status_code == 201


async def test_user_cancel_join_request(
    client: TestClient, company_requests, user_tests_token
):
    response = client.delete(
        f"/user/cancel_join_request/{company_requests[1].id}",
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )

    assert response.status_code == 204


async def test_user_company_leave(
    client: TestClient, users, companies, company_requests
):
    response = client.post(
        "/auth/login",
        json={"email": test_user_leave.email, "password": test_user_leave.password},
    )
    token = response.json()["token"]
    response = client.delete(
        f"/user/{companies[0].id}/leave", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204


async def test_user_list_invites(client: TestClient, users):
    response = client.post(
        "/auth/login",
        json={"email": test_user_leave.email, "password": test_user_leave.password},
    )
    token = response.json()["token"]
    response = client.get(
        f"/user/{users[3].id}/invites", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


async def test_user_list_join_requests(client: TestClient, users):
    response = client.post(
        "/auth/login",
        json={"email": test_user_leave.email, "password": test_user_leave.password},
    )
    token = response.json()["token"]
    response = client.get(
        f"/user/{users[3].id}/join_requests",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
