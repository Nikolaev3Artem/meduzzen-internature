from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import test_database_url
from app.db.alchemy.models import Base
from app.db.postgress import get_session
from app.main import app

engine_test = create_async_engine(
    test_database_url, echo=True, future=True, poolclass=NullPool
)
async_session = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)


async def override_get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@fixture
async def session():
    async with async_session() as session:
        yield session


@fixture(name="client", scope="session")
def client_fixture():
    client = TestClient(app)
    yield client
