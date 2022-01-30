import pytest


@pytest.fixture(scope="session")
def API_URL():
    return "http://127.0.0.1:5000"
