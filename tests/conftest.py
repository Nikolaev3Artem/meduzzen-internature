from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.core.config import settings
from app.db.postgress import get_session
from app.main import app
from app.db.alchemy.models import Base
import subprocess
import time

test_database_url = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}_test"
engine_test = create_async_engine(test_database_url, echo=True)
async_session = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)
Base.metadata.bind = engine_test


async def override_get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@fixture(scope="session", autouse=True)
async def prepare_database():
    subprocess.run(
        ["docker-compose", "-f", "docker-compose-test.yml", "up", "-d", "--build"]
    )
    time.sleep(2)
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    subprocess.run(["docker-compose", "-f", "docker-compose-test.yml", "down"])


@fixture(name="client", scope="session")
def client_fixture():
    client = TestClient(app)
    return client
