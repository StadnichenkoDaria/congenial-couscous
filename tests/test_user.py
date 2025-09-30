import json

import pytest
from fastapi import status
import requests
from models.user import User


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    for user in users:
        User.model_validate(user)


def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_user(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK

    user = response.json()
    User.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "qwerty"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user(app_url):
    new_user = {
        "name": "morpheus",
        "job": "leader"
    }

    response = requests.post(f"{app_url}/api/users", json=new_user)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data["name"] == new_user["name"]
    assert response_data["job"] == new_user["job"]
    assert "id" in response_data
    assert "createdAt" in response_data

    with open("../users.json", "r") as f:
        users = json.load(f)
        assert len(users) == 13


def test_update_user_put(app_url):
    user_id = 1
    get_response = requests.get(f"{app_url}/api/users/{user_id}")
    original_user = get_response.json()

    updated_data = {
        "id": user_id,
        "email": original_user["email"],
        "first_name": "George Updated",
        "last_name": original_user["last_name"],
        "avatar": original_user["avatar"]
    }
    update_response = requests.put(f"{app_url}/api/users/{user_id}", json=updated_data)
    assert update_response.status_code == status.HTTP_200_OK

    get_updated_response = requests.get(f"{app_url}/api/users/{user_id}")
    updated_user = get_updated_response.json()
    assert updated_user["first_name"] == "George Updated"


def test_delete_user(app_url):
    user_id = 1
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
