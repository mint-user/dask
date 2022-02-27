import pytest
import requests

from app import db
from app.tasks.models import Task


@pytest.fixture(params=[
    ({"name": "", "parent_task_id": 1}, 400, "Task name should not be empty"),
    ({"name": "     ", "parent_task_id": 1}, 400, "Task name should not be empty"),
    ({"name": "simple", "parent_task_id": 1}, 400, "You do not have task with id=1 to make it parent"),
    ({"name": "simple"}, 201, "new task has been created"),
    ({"name": "simple2", "parent_task_id": 1}, 201, "new task has been created"),
                        ])
def task_creation_validation_data(request):
    return request.param


# @pytest.fixture(scope="class")
# def user_with_no_tasks_loggen_in(sure_user_exists, API_URL, testuser_data, request):
#     user = sure_user_exists
#     user_tasks = Task.query.filter(Task.user_id == user.id).all()
#     for user_task in user_tasks:
#         db.session.delete(user_task)
#     db.session.commit()
#     resp = requests.post(f"{API_URL}/api/v1/accounts/session", json={"email": testuser_data['email'],
#                                                                      "password": testuser_data['password']})
#     cookies = resp.cookies.get_dict()
#     assert "access_token_cookie" in cookies.keys()
#     # return cookies
#     request.cls.cookies = cookies
#     yield
