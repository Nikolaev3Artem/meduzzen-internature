from httpx import AsyncClient


async def test_healthcheck(ac: AsyncClient):
    response = await ac.get("healthcheck/")
    assert response.status_code == 200
    assert response.json() == {"status_code": 200, "detail": "ok", "result": "working"}
