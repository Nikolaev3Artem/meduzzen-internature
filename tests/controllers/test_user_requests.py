from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.enums import RequestStatus
from app.db.alchemy.models import Company, CompanyRequests, User
from tests.constants import test_user_leave


async def test_user_accept_invite(
    client: TestClient, prepare_database, fill_database, user_tests_token, session
):
    test_invite = await session.execute(
        select(CompanyRequests).where(
            CompanyRequests.status == RequestStatus.INVITATION.value
        )
    )
    test_invite_id = test_invite.scalar().id
    response = client.post(
        f"/user/{test_invite_id}/accept_invite",
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )

    assert response.status_code == 200


async def test_user_reject_invite(
    client: TestClient, prepare_database, fill_database, user_tests_token, session
):
    test_invite = await session.execute(
        select(CompanyRequests).where(
            CompanyRequests.status == RequestStatus.INVITATION.value
        )
    )
    test_invite_id = test_invite.scalar().id
    response = client.delete(
        f"/user/{test_invite_id}/reject_invite",
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )

    assert response.status_code == 204


async def test_user_send_join_request(
    client: TestClient, prepare_database, fill_database, user_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(1))
    test_company_id = test_company.scalar().id
    response = client.post(
        f"/user/{test_company_id}/send_join_request",
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )

    assert response.status_code == 201


async def test_user_cancel_join_request(
    client: TestClient, prepare_database, fill_database, user_tests_token, session
):
    test_invite = await session.execute(select(CompanyRequests).limit(1).offset(0))
    test_invite_id = test_invite.scalar().id
    response = client.delete(
        f"/user/cancel_join_request/{test_invite_id}",
        headers={"Authorization": f"Bearer {user_tests_token}"},
    )

    assert response.status_code == 204


async def test_user_company_leave(
    client: TestClient, prepare_database, fill_database, session
):
    response = client.post(
        "/auth/login",
        json={"email": test_user_leave.email, "password": test_user_leave.password},
    )
    token = response.json()["token"]
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id
    response = client.delete(
        f"/user/{test_company_id}/leave", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204


async def test_user_list_invites(
    client: TestClient, prepare_database, fill_database, user_tests_token, session
):
    response = client.post(
        "/auth/login",
        json={"email": test_user_leave.email, "password": test_user_leave.password},
    )
    token = response.json()["token"]
    test_user = await session.execute(select(User).limit(1).offset(3))
    test_user_id = test_user.scalar().id
    response = client.get(
        f"/user/{test_user_id}/invites", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


async def test_user_list_join_requests(
    client: TestClient, prepare_database, fill_database, session
):
    response = client.post(
        "/auth/login",
        json={"email": test_user_leave.email, "password": test_user_leave.password},
    )
    token = response.json()["token"]
    test_user = await session.execute(select(User).limit(1).offset(3))
    test_user_id = test_user.scalar().id
    response = client.get(
        f"/user/{test_user_id}/join_requests",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
