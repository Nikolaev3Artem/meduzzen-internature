import os

import alembic
from alembic.config import Config
from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app


@fixture(scope="session")
def apply_migrations():
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client
