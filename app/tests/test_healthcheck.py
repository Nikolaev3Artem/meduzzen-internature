from fastapi.testclient import TestClient


def test_healthcheck(client: TestClient):
    response = client.get("healthcheck/")
    assert response.status_code == 200
    assert response.json() == {"status_code": 200, "detail": "ok", "result": "working"}


def test_healthcheck_postgress(client: TestClient):
    response = client.get("healthcheck/postgress/")
    assert response.status_code == 200
    assert response.json() == {
        "status_code": 200,
        "detail": "ok",
        "result": "postgress working",
    }
