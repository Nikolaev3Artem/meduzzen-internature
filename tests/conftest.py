from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.alchemy.models import Base, Company, CompanyRequests, Quiz, User
from app.db.postgress import get_session
from app.main import app
from tests.constants import (
    companies_list,
    quiz_list,
    requests,
    test_company_owner_login,
    test_user_login,
    users_list,
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
async def set_up_users(session):
    await session.execute(insert(User).values(users_list))
    await session.commit()


@fixture(scope="function")
async def set_up_companies(users, session):
    for company in companies_list:
        company["owner_id"] = users[0].id
    await session.execute(insert(Company).values(companies_list))
    await session.commit()


@fixture(scope="function")
async def set_up_company_requests(users, companies, session):
    for index, user in enumerate(requests):
        user["user_id"] = users[index].id
        user["company_id"] = companies[0].id
    await session.execute(insert(CompanyRequests).values(requests))
    await session.commit()


@fixture(scope="function")
async def set_up_quizzes(companies, session):
    for index, quiz in enumerate(quiz_list):
        quiz["company_id"] = companies[0].id
    await session.execute(insert(Quiz).values(quiz_list))
    await session.commit()


@fixture(scope="function", name="users")
async def users(prepare_database, set_up_users, session):
    users = await session.execute(select(User))
    yield users.scalars().all()


@fixture(scope="function", name="companies")
async def companies(prepare_database, set_up_companies, session):
    companies = await session.execute(select(Company))
    yield companies.scalars().all()


@fixture(scope="function", name="company_requests")
async def company_requests(prepare_database, set_up_company_requests, session):
    company_requests = await session.execute(select(CompanyRequests))
    yield company_requests.scalars().all()


@fixture(scope="function", name="quizzes")
async def quizzes(prepare_database, set_up_quizzes, session):
    quizzes = await session.execute(select(Quiz))
    yield quizzes.scalars().all()


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


@fixture(name="client", scope="session")
def client_fixture():
    client = TestClient(app)
    yield client


@fixture
async def session():
    async with async_session() as session:
        yield session
