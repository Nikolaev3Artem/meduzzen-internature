from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.enums import RequestStatus
from app.db.alchemy.models import Company, CompanyRequests, User
from tests.constants import users


async def test_company_send_invite(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id
    test_user = await session.execute(select(User).limit(1).offset(0))
    test_user_id = test_user.scalar().id
    response = client.post(
        f"/company/{test_company_id}/send_invite/{test_user_id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 201


async def test_company_delete_invite(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id
    test_invite = await session.execute(
        select(CompanyRequests).where(
            CompanyRequests.status == RequestStatus.INVITATION.value
        )
    )
    test_invite_id = test_invite.scalar().id
    response = client.delete(
        f"/company/{test_company_id}/cancel_invite/{test_invite_id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 204


async def test_company_accept_join_request(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id
    test_invite = await session.execute(select(CompanyRequests).limit(1).offset(1))
    test_invite_id = test_invite.scalar().id
    response = client.post(
        f"/company/{test_company_id}/accept_join_request/{test_invite_id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 200


async def test_company_reject_join_request(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id
    test_invite = await session.execute(select(CompanyRequests).limit(1).offset(1))
    test_invite_id = test_invite.scalar().id
    response = client.delete(
        f"/company/{test_company_id}/reject_join_request/{test_invite_id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 204


async def test_company_kick_member(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id
    test_member = await session.execute(select(User).limit(1).offset(3))
    test_member_id = test_member.scalar().id
    response = client.delete(
        f"/company/{test_company_id}/kick/{test_member_id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 204


async def test_company_get_invites_list(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id

    response = client.get(
        f"/company/{test_company_id}/invitations",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]["username"] == users[1]["username"]
    assert response_data[0]["email"] == users[1]["email"]


async def test_company_get_join_requests_list(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id

    response = client.get(
        f"/company/{test_company_id}/join_requests",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]["username"] == users[2]["username"]
    assert response_data[0]["email"] == users[2]["email"]


async def test_company_get_members_list(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id

    response = client.get(
        f"/company/{test_company_id}/members",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]["username"] == users[3]["username"]
    assert response_data[0]["email"] == users[3]["email"]


async def test_company_promote_to_admin(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id

    test_user = await session.execute(select(User).limit(1).offset(3))
    test_user_id = test_user.scalar().id

    response = client.patch(
        f"/company/{test_company_id}/update_member_role/{test_user_id}?member_role=admin",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )

    assert response.status_code == 200


async def test_company_demotion_admin_to_member(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id

    test_user = await session.execute(select(User).limit(1).offset(4))
    test_user_id = test_user.scalar().id

    response = client.patch(
        f"/company/{test_company_id}/update_member_role/{test_user_id}?member_role=member",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )

    assert response.status_code == 200


async def test_company_admins_list(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id

    response = client.get(
        f"/company/{test_company_id}/admins",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )

    assert response.status_code == 200
