from httpx import AsyncClient


async def test_healthcheck(client: AsyncClient):
    response = client.get("healthcheck/")
    assert response.status_code == 200
    assert response.json() == {"status_code": 200, "detail": "ok", "result": "working"}
