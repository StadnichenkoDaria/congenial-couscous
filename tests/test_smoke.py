import requests
from fastapi import status


def test_service_is_up(app_url):
    response = requests.get(app_url)
    assert response.status_code == status.HTTP_200_OK


def test_status(app_url):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert "users" in response.json()
    assert response_json["users"] is True

