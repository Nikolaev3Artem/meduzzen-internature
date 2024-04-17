from fastapi.testclient import TestClient


def test_healthcheck(client: TestClient):
    response = client.get("healthcheck/")
    assert response.status_code == 200
    assert response.json() == {"status_code": 200, "detail": "ok", "result": "working"}
