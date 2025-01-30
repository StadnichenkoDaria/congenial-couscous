import pytest


@pytest.mark.parametrize("email, password, expected_token", [
    ("eve.holt@reqres.in", "cityslicka", "QpwL5tke4Pnpja7X4"),
])
def test_login_success(email, password, expected_token, api):
    response = api.login(email, password)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    body = response.json()
    assert "token" in body, f"Response body does not contain 'token' key"
    assert body["token"] == expected_token, f"Expected token {expected_token}, but got {body['token']}"


@pytest.mark.parametrize("email, password, expected_error", [
    ("peter@klaven", "", "Missing password"),
])
def test_login_unsuccessful(email, password, expected_error, api):
    response = api.login(email, password)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"

    body = response.json()
    assert "error" in body, "Response body does not contain 'error' key"
    assert body["error"] == expected_error, f"Expected error message '{expected_error}', but got '{body['error']}'"
