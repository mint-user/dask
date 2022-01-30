import requests


class TestUserCreation:

    def test_success_creation(self, API_URL):
        # resp = requests.get("http://127.0.0.1:5000")
        resp = requests.get(API_URL)
        print(resp.text)
        assert resp.status_code == 200
