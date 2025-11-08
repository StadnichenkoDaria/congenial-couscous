import json
import os

import pytest
from fastapi import status
import requests
from app.models.user import User, UsersResponse


@pytest.fixture(scope="module")
def fill_test_data(app_url):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_users = os.path.join(current_dir, "..", "users.json")

    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")


@pytest.fixture
def user_list(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def test_users(app_url, fill_test_data):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    users_list = data['items']
    for user in users_list:
        User.model_validate(user)


def test_users_no_duplicates(user_list, fill_test_data):
    users_data = user_list['items']
    users_ids = [user['id'] for user in users_data]
    assert len(users_ids) == len(set(users_ids))


def test_user_id(app_url, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        user = response.json()
        User.model_validate(user)


@pytest.mark.parametrize("user_id", [1000000])
def test_user_nonexistent_values(app_url, user_id, fill_test_data):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "qwerty"])
def test_user_invalid_values(app_url, user_id, fill_test_data):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("page, expected_size, expected_page", [
    (None, 12, 1),  # без параметра page
    (1, 12, 1),  # page=1
    (2, 0, 2),  # page=2
])
def test_pagination_items_count_matches_size(app_url, page, expected_size, expected_page, fill_test_data):
    params = {'page': page} if page is not None else {}
    response = requests.get(f"{app_url}/api/users", params=params)
    assert response.status_code == status.HTTP_200_OK
    users_response = UsersResponse.model_validate(response.json())
    assert len(users_response.items) == expected_size
    assert users_response.page == expected_page


@pytest.mark.parametrize("page", [3, 100])
def test_pagination_out_of_range_pages_returns_empty_items(app_url, page, fill_test_data):
    response = requests.get(f"{app_url}/api/users", params={'page': page})
    assert response.status_code == status.HTTP_200_OK
    users_response = UsersResponse.model_validate(response.json())

    assert users_response.items == []
    assert users_response.total == 12
    assert users_response.page == page
    assert users_response.size == 50
    assert users_response.pages == 1


def test_pagination_invalid_page_string_returns_parsing_error(app_url, fill_test_data):
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
def test_pagination_different_sizes_correct_pages_calculation(app_url, size, expected_pages, fill_test_data):
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


def test_create_user(app_url, fill_test_data):
    response = requests.get(f"{app_url}/api/users")
    initial_data = response.json()
    all_users = initial_data['items']
    max_id = max(user['id'] for user in all_users)
    expected_new_id = max_id + 1
    initial_count = len(all_users)

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

    assert response_data["id"] == expected_new_id

    response = requests.get(f"{app_url}/api/users")
    updated_data = response.json()
    updated_users = updated_data['items']

    assert len(updated_users) == initial_count + 1

    new_user_in_db = next((u for u in updated_users if u['id'] == expected_new_id), None)
    assert new_user_in_db is not None
    assert new_user_in_db['email'] == new_user['email']
    assert new_user_in_db['first_name'] == new_user['first_name']


def test_update_user(app_url, fill_test_data):
    user_id = fill_test_data[0]

    updated_data = {
        "first_name": "George Updated"
    }

    update_response = requests.patch(f"{app_url}/api/users/{user_id}", json=updated_data)
    assert update_response.status_code == status.HTTP_200_OK

    get_updated_response = requests.get(f"{app_url}/api/users/{user_id}")
    updated_user = get_updated_response.json()
    assert updated_user["first_name"] == "George Updated"


def test_delete_users(app_url, fill_test_data):
    response = requests.get(f"{app_url}/api/users")
    data = response.json()
    users_list = data['items']
    user_ids = [user["id"] for user in users_list]
    for user_id in user_ids:
        delete_response = requests.delete(f"{app_url}/api/users/{user_id}")
        print(f"Deleting user {user_id}: {delete_response.status_code}")
        assert delete_response.status_code in [204, 200]

    response = requests.get(f"{app_url}/api/users")
    data = response.json()
    assert len(data['items']) == 0
    print("All users deleted successfully")
