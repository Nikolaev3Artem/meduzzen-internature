import asyncio
import os
from typing import AsyncGenerator

from httpx import AsyncClient
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.postgress import get_session
from app.main import app

test_database_url = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:5432/{settings.postgres_db}_test"
engine = create_async_engine(test_database_url, future=True, echo=True)
test_async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def override_get_session() -> AsyncSession:
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@fixture(scope="session", autouse=True)
def run_migrations():
    os.system("alembic upgrade head")
    yield
    os.system("alembic downgrade base")


@fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://localhost") as asclient:
        yield asclient
