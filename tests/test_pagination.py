import pytest
import requests
from fastapi import status


def test_pagination_default_params(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'total' in data
    assert 'page' in data
    assert 'size' in data
    assert 'pages' in data


@pytest.mark.parametrize("page, expected_size, expected_page", [
    (None, 12, 1),  # без параметра page
    (1, 6, 1),  # page=1
    (2, 6, 2),  # page=2
])
def test_pagination_items_count_matches_size(app_url, page, expected_size, expected_page):
    params = {'page': page} if page is not None else {}
    response = requests.get(f"{app_url}/api/users", params=params)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data['items']) == expected_size


@pytest.mark.parametrize("page", [3, 100])
def test_pagination_out_of_range_pages_returns_empty_items(app_url, page):
    response = requests.get(f"{app_url}/api/users", params={'page': page})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data['items'] == []
    assert data['total'] == 12
    assert data['page'] == page
    assert data['size'] == 6
    assert data['pages'] == 2


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
    data = response.json()
    assert len(data['items']) == size
    assert data['total'] == 12
    assert data['page'] == 1
    assert data['size'] == size
    assert data['pages'] == expected_pages
    assert len(data['items']) == size
