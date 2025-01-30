import pytest
from app.data import users_db
from fastapi import status


def test_get_users(api):
    response = api.get_users()
    assert response.status_code == 200
    data = response.json()
    assert data['page'] == 1
    assert data['per_page'] == 6
    assert data['total'] == len(users_db)
    assert data['total_pages'] == 1
    assert len(data['data']) == 6


@pytest.mark.parametrize("user_id, expected_email", [
    (2, "janet.weaver@reqres.in"),
    (4, "eve.holt@reqres.in"),
    (6, "tracey.ramos@reqres.in"),
])
def test_user_data(user_id, expected_email, api):
    response = api.get_user(user_id)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    body = response.json()
    assert "data" in body, f"Response body does not contain 'data' key"

    data = body["data"]
    assert data["id"] == user_id, f"Expected id {user_id}, but got {data['id']}"
    assert data["email"] == expected_email, f"Expected email {expected_email}, but got {data['email']}"


def test_create_user(client, api):
    payload = {
        "name": "morpheus",
        "job": "leader"
    }
    response = api.create_user(payload)
    assert response.status_code == status.HTTP_201_CREATED, f"Expected status code 201, but got {response.status_code}"

    body = response.json()

    assert body["name"] == payload["name"], f"Expected name '{payload['name']}', but got '{body['data']['name']}'"
    assert body["job"] == payload["job"], f"Expected job '{payload['job']}', but got '{body['data']['job']}'"


def test_update_user_put(client, api):
    user_id = 2
    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = api.update_user_put(user_id, payload)
    assert response.status_code == status.HTTP_200_OK, f"Expected status code 200, but got {response.status_code}"

    body = response.json()

    assert body["name"] == payload["name"], f"Expected name '{payload['name']}', but got '{body['name']}'"
    assert body["job"] == payload["job"], f"Expected job '{payload['job']}', but got '{body['job']}'"


def test_update_user_patch(client, api):
    user_id = 2
    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = api.update_user_patch(user_id, payload)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    body = response.json()
    assert "name" in body, "Response body does not contain 'name' field"
    assert "job" in body, "Response body does not contain 'job' field"
    assert "updatedAt" in body, "Response body does not contain 'updatedAt' field"
    assert body["name"] == payload["name"], f"Expected name '{payload['name']}', but got '{body['name']}'"
    assert body["job"] == payload["job"], f"Expected job '{payload['job']}', but got '{body['job']}'"


def test_delete_user(client, api):
    user_id = 2

    response = api.delete_user(user_id)
    assert response.status_code == 204, f"Expected status code 204, but got {response.status_code}"
