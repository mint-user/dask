import pytest
from faker import Faker
from faker.providers import lorem


fake = Faker()
fake.add_provider(lorem)

task_name = fake.sentence()

@pytest.fixture(params=[
    ({"name": "", "parent_task_id": 1}, 400, "Task name should not be empty"),
    ({"name": "     ", "parent_task_id": 1}, 400, "Task name should not be empty"),
    ({"name": task_name, "parent_task_id": 1}, 400, "You do not have task with id=1 to make it parent"),
    ({"name": task_name}, 201, "new task has been created"),
    ({"name": fake.sentence(), "parent_task_id": 1}, 201, "new task has been created"),
                        ])
def task_creation_validation_data(request):
    return request.param
