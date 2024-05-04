from fastapi.testclient import TestClient

from tests.constants import quiz_create, quiz_list, quiz_update


def test_quizzes_get_list(client: TestClient, companies, quizzes, company_tests_token):
    response = client.get(
        f"/quiz/{companies[0].id}/quiz_list?limit=3&offset=0",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 3
    for index, quiz in enumerate(response_data):
        assert quiz["name"] == quiz_list[index]["name"]
        assert quiz["description"] == quiz_list[index]["description"]
        assert quiz["questions"] == quiz_list[index]["questions"]


def test_quizzes_create(client: TestClient, companies, quizzes, company_tests_token):
    response = client.post(
        f"/quiz/{companies[0].id}/create_quiz",
        json={
            "name": quiz_create["name"],
            "description": quiz_create["description"],
            "questions": quiz_create["questions"],
        },
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["name"] == quiz_create["name"]
    assert response_data["description"] == quiz_create["description"]
    assert response_data["questions"] == quiz_create["questions"]


def test_quizzes_update(client: TestClient, companies, quizzes, company_tests_token):
    response = client.patch(
        f"/quiz/{quizzes[0].id}/update_quiz/{companies[0].id}",
        json={"name": quiz_update["name"]},
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["name"] == quiz_update["name"]


def test_quizzes_delete(client: TestClient, companies, quizzes, company_tests_token):
    response = client.delete(
        f"/quiz/{quizzes[0].id}/delete_quiz/{companies[0].id}",
        headers={"Authorization": f"Bearer {company_tests_token}"},
    )
    assert response.status_code == 204
