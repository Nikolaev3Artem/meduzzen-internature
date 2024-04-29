from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db.alchemy.models import Company
from tests.constants import (
    companies,
    company_updated_name,
    test_company_create_description,
    test_company_create_name,
)


def test_company_get_list(
    client: TestClient, prepare_database, fill_database, company_tests_token
):
    response = client.get(
        "/company/?limit=3&offset=0",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 3
    for index, company in enumerate(companies):
        assert response_data[index]["name"] == company["name"]
        assert response_data[index]["description"] == company["description"]


def test_company_create(
    client: TestClient, prepare_database, fill_database, company_tests_token
):
    response = client.post(
        "/company",
        json={
            "name": test_company_create_name,
            "description": test_company_create_description,
        },
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["name"] == test_company_create_name
    assert response_data["description"] == test_company_create_description


async def test_company_update(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(
        select(Company).where(Company.visible == True).limit(1).offset(0)
    )
    test_company_id = test_company.scalar().id
    response = client.patch(
        f"/company/{test_company_id}",
        json={"name": company_updated_name},
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["name"] == company_updated_name


async def test_company_delete(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(
        select(Company).where(Company.visible == True).limit(1).offset(0)
    )
    test_company_id = test_company.scalar().id
    response = client.delete(
        f"/company/{test_company_id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 204


async def test_company_get(
    client: TestClient, prepare_database, fill_database, company_tests_token, session
):
    test_company = await session.execute(
        select(Company).where(Company.visible == True).limit(1).offset(0)
    )
    test_company_id = test_company.scalar().id
    response = client.get(
        f"/company/{test_company_id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["name"] == companies[0]["name"]
    assert response_data["description"] == companies[0]["description"]
