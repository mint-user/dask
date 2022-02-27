import json
import pytest
import requests


# @pytest.mark.usefixtures("API_URL")
class TestNotLoggedInTasksValidationsCRUD:

    # def test_server_is_up(self, API_URL):
    def test_server_is_up(self, API_URL):
        resp = requests.get(API_URL)
        assert resp.status_code == 200

    @pytest.mark.parametrize("resp_type, data", [
        ("post", {"name": "newC task", "parent_task_id": 1}),
        ("get", {"name": "newC task", "parent_task_id": 1}),
        ("delete", {"name": "newC task", "parent_task_id": 1}),
    ])
    def test_forbid_tasks_crud_for_not_authenticated(self, API_URL, resp_type, data):
        req = getattr(requests, resp_type)
        if resp_type == "delete":
            resp = req(f"{API_URL}/api/v1/tasks")
        else:
            resp = req(f"{API_URL}/api/v1/tasks", data)

        assert resp.json()["msg"] == 'Missing cookie "access_token_cookie"'


@pytest.mark.usefixtures("user_with_no_tasks_loggen_in")
class TestLoggedInTasksValidationsCRUD:



    # @classmethod
    # def setup_class(cls, delete_all_user_tasks):
    #     pass

    @pytest.mark.parametrize("data", [pytest.lazy_fixture("task_creation_validation_data")])
    def test_creation_tasks_validation(self, API_URL, data):
        logged_in_cookies = self.cookies
        data, code, message = data
        resp = requests.post(f"{API_URL}/api/v1/tasks", json.dumps(data),
                             cookies=logged_in_cookies)
        # print(resp.text)
        assert resp.status_code == code
        if code == 201:
            assert resp.json()["msg"] == message
        else:
            assert resp.json()["msg"][0]["msg"] == message


