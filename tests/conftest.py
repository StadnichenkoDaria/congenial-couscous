import pytest
from api.reqres_api import ReqresAPI
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def api():
    return ReqresAPI()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
