import os
import dotenv
import pytest
from api.reqres_api import ReqresAPI


@pytest.fixture
def api():
    return ReqresAPI()


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")
