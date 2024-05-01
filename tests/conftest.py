from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.alchemy.models import Base, Company, CompanyRequests, User
from app.db.postgress import get_session
from app.main import app
from tests.constants import (
    companies,
    requests,
    test_company_owner_login,
    test_user_login,
    users,
)

engine_test = create_async_engine(
    settings.test_database_url, echo=True, future=True, poolclass=NullPool
)
async_session = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)


async def override_get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@fixture(scope="function")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@fixture(scope="function")
async def fill_database(session):
    await session.execute(insert(User).values(users))
    await session.commit()
    test_user = await session.execute(select(User).limit(1).offset(0))
    test_user_id = test_user.scalar().id
    for company in companies:
        company["owner_id"] = test_user_id
    await session.execute(insert(Company).values(companies))
    await session.commit()

    test_users = await session.execute(select(User).limit(3).offset(1))
    test_users = test_users.scalars().all()
    test_company = await session.execute(select(Company).limit(1).offset(0))
    test_company_id = test_company.scalar().id

    for index, user in enumerate(requests):
        user["user_id"] = test_users[index].id
        user["company_id"] = test_company_id
    await session.execute(insert(CompanyRequests).values(requests))
    await session.commit()
    yield


@fixture(scope="function")
async def company_tests_token(session, client: TestClient):
    response = client.post(
        "/auth/login",
        json={
            "email": test_company_owner_login.email,
            "password": test_company_owner_login.password,
        },
    )
    token = response.json()["token"]
    yield token


@fixture(scope="function")
async def user_tests_token(session, client: TestClient):
    response = client.post(
        "/auth/login",
        json={"email": test_user_login.email, "password": test_user_login.password},
    )
    token = response.json()["token"]
    yield token


@fixture
async def session():
    async with async_session() as session:
        yield session


@fixture(name="client", scope="session")
def client_fixture():
    client = TestClient(app)
    yield client
