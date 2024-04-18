import os
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.postgress import get_session
from app.main import app

test_database_url = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}_test"
engine_test = create_async_engine(test_database_url, future=True, echo=True)
test_async_session = sessionmaker(
    engine_test, expire_on_commit=False, class_=AsyncSession
)


async def override_get_session() -> AsyncSession:
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@fixture(scope="session", autouse=True)
def setup_docker():
    # os.system("docker-compose -f docker-compose-test.yml up -d --build")
    # time.sleep(2)
    os.system("alembic upgrade head")
    yield
    # os.system("docker-compose -f docker-compose-test.yml down")


@fixture(name="client", scope="session")
def client_fixture():
    client = TestClient(app)
    yield client
