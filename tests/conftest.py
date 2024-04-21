from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.alchemy.models import Base, User
from app.db.postgress import get_session
from app.main import app
from tests.constants import users

engine_test = create_async_engine(
    settings.test_database_url, echo=True, future=True, poolclass=NullPool
)
async_session = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)


async def override_get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@fixture
async def session():
    async with async_session() as session:
        yield session


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
    yield


@fixture(name="client", scope="session")
def client_fixture():
    client = TestClient(app)
    yield client
