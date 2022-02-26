import pytest
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

@pytest.fixture(scope="module")
def delete_all_tasks():
    # user = get_user_by_email(email)
    Task.query.delete()
    # if user is not None:
    #     db.session.delete(user)
    #     db.session.commit()