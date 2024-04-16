from fastapi.testclient import TestClient


def test_user_create(client: TestClient):
    # test_data =
    response = client.post(
        "user/create/",
        json={
            "email": "testemail@gmail.com",
            "username": "test_username",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    # assert response.json() == {"test_username","testemail@gmail.com","$2b$12$L3GaFTLL8spMuiF3GnTD9OGPmnUBBlLL4MO047NmM8M.tVi8eNZjm","d56a9112-15ba-4199-9d2e-44ab7ab90b2c"}
