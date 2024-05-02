from fastapi.testclient import TestClient

from tests.constants import users_list


def test_company_send_invite(client: TestClient, companies, users, company_tests_token):
    response = client.post(
        f"/company/{companies[0].id}/send_invite/{users[0].id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 201


async def test_company_delete_invite(
    client: TestClient, companies, company_requests, company_tests_token
):
    response = client.delete(
        f"/company/{companies[0].id}/cancel_invite/{company_requests[0].id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 204


async def test_company_accept_join_request(
    client: TestClient, companies, company_requests, company_tests_token
):
    response = client.post(
        f"/company/{companies[0].id}/accept_join_request/{company_requests[1].id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 200


async def test_company_reject_join_request(
    client: TestClient, companies, company_requests, company_tests_token
):
    response = client.delete(
        f"/company/{companies[0].id}/reject_join_request/{company_requests[1].id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 204


async def test_company_kick_member(
    client: TestClient, companies, users, set_up_company_requests, company_tests_token
):
    response = client.delete(
        f"/company/{companies[0].id}/kick/{users[2].id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 204


async def test_company_get_invites_list(
    client: TestClient, companies, set_up_company_requests, company_tests_token
):
    response = client.get(
        f"/company/{companies[0].id}/invitations",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]["username"] == users_list[0]["username"]
    assert response_data[0]["email"] == users_list[0]["email"]


async def test_company_get_join_requests_list(
    client: TestClient, companies, set_up_company_requests, company_tests_token
):
    response = client.get(
        f"/company/{companies[0].id}/join_requests",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]["username"] == users_list[1]["username"]
    assert response_data[0]["email"] == users_list[1]["email"]


async def test_company_get_members_list(
    client: TestClient, companies, set_up_company_requests, company_tests_token
):
    response = client.get(
        f"/company/{companies[0].id}/members",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]["username"] == users_list[2]["username"]
    assert response_data[0]["email"] == users_list[2]["email"]


async def test_company_promote_to_admin(
    client: TestClient, companies, users, set_up_company_requests, company_tests_token
):
    response = client.patch(
        f"/company/{companies[0].id}/update_member_role/{users[2].id}?member_role=admin",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )

    assert response.status_code == 200


async def test_company_demotion_admin_to_member(
    client: TestClient, companies, users, set_up_company_requests, company_tests_token
):
    response = client.patch(
        f"/company/{companies[0].id}/update_member_role/{users[3].id}?member_role=member",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )

    assert response.status_code == 200


async def test_company_admins_list(
    client: TestClient, companies, set_up_company_requests, company_tests_token
):
    response = client.get(
        f"/company/{companies[0].id}/admins",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )

    assert response.status_code == 200
