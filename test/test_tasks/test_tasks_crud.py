import json

import pytest
from requests import Request

import requests


class TestTasksCRUD:

    def test_server_is_up(self, API_URL):
        resp = requests.get(API_URL)
        assert resp.status_code == 200

    def test_creation_tasks_validation(self, logged_in_cookies, API_URL):
        resp = requests.post(f"{API_URL}/api/v1/tasks", json.dumps({"name": "", "parent_task_id": 1}),
                             cookies=logged_in_cookies)
        print(resp.text)
        assert resp.json()["msg"][0]["msg"] == 'Task name should not be empty'

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
