from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app

# @fixture(scope="session")
# async def setup_db():
#     settings.testing = True
#     config = Config("./../alembic.ini")

#     await alembic.command.upgrade(config, "head")


@fixture(name="client", scope="session")
def client_fixture():
    client = TestClient(app)
    yield client
