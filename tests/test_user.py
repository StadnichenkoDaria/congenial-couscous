import json
import os

import pytest
from fastapi import status
import requests
from models.user import User, UsersResponse


@pytest.fixture
def user_list(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    users_response = UsersResponse.model_validate(data)
    return users_response.items


def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    UsersResponse.model_validate(data)


def test_users_no_duplicates(user_list):
    users_ids = [user.id for user in user_list]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_user_id(app_url, user_id):
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


@pytest.mark.parametrize("page, expected_size, expected_page", [
    (None, 12, 1),  # без параметра page
    (1, 6, 1),  # page=1
    (2, 6, 2),  # page=2
])
def test_pagination_items_count_matches_size(app_url, page, expected_size, expected_page):
    params = {'page': page} if page is not None else {}
    response = requests.get(f"{app_url}/api/users", params=params)
    assert response.status_code == status.HTTP_200_OK
    users_response = UsersResponse.model_validate(response.json())
    assert len(users_response.items) == expected_size
    assert users_response.page == expected_page


@pytest.mark.parametrize("page", [3, 100])
def test_pagination_out_of_range_pages_returns_empty_items(app_url, page):
    response = requests.get(f"{app_url}/api/users", params={'page': page})
    assert response.status_code == status.HTTP_200_OK
    users_response = UsersResponse.model_validate(response.json())

    assert users_response.items == []
    assert users_response.total == 12
    assert users_response.page == page
    assert users_response.size == 6
    assert users_response.pages == 2


def test_pagination_invalid_page_string_returns_parsing_error(app_url):
    response = requests.get(f"{app_url}/api/users", params={'page': 'qwe'})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    error_detail = data['detail'][0]
    assert error_detail['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
    assert error_detail['input'] == 'qwe'


@pytest.mark.parametrize("size,expected_pages", [
    (1, 12),
    (10, 2),
    (12, 1),
])
def test_pagination_different_sizes_correct_pages_calculation(app_url, size, expected_pages):
    response = requests.get(f"{app_url}/api/users", params={'size': size})
    assert response.status_code == status.HTTP_200_OK
    users_response = UsersResponse.model_validate(response.json())
    assert len(users_response.items) == size
    assert users_response.total == 12
    assert users_response.page == 1
    assert users_response.size == size
    assert users_response.pages == expected_pages
    for user in users_response.items:
        User.model_validate(user)


def test_create_user(app_url):
    response = requests.get(f"{app_url}/api/users")
    initial_data = response.json()
    initial_count = initial_data['total']
    expected_new_id = initial_count + 1

    new_user = {
        "email": "morpheus@reqres.in",
        "first_name": "Morpheus",
        "last_name": "Leader",
        "avatar": "https://reqres.in/img/faces/1-image.jpg"
    }

    response = requests.post(f"{app_url}/api/users", json=new_user)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    assert response_data["email"] == new_user["email"]
    assert response_data["first_name"] == new_user["first_name"]
    assert response_data["last_name"] == new_user["last_name"]
    assert response_data["avatar"] == new_user["avatar"]
    assert "id" in response_data
    assert "createdAt" in response_data

    assert response_data["id"] == expected_new_id

    users_json_path = os.path.join(os.path.dirname(__file__), "..", "users.json")

    with open(users_json_path, "r") as f:
        users = json.load(f)
        assert len(users) == initial_count + 1


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
    user_id = 12
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
