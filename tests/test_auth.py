import requests


def test_login_success(app_url):
    response = requests.post(f"{app_url}/api/login", json={"email": "eve.holt@reqres.in", "password": "cityslicka"})

    assert response.status_code == 200
    assert response.json() == {"token": "QpwL5tke4Pnpja7X4"}


def test_login_unsuccessful(app_url):
    response = requests.post(f"{app_url}/api/login", json={"email": "wrong@example.com", "password": "cityslicka"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid login credentials"}
