import collections
import json
from typing import Optional

from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from pydantic import BaseModel, ValidationError
from sqlalchemy import select

from app import app, db
from app.auth.models import User
from app.tasks.models import Task
from app.tasks import tasks

from flask import request, jsonify, render_template, make_response


jwt = JWTManager(app)


@tasks.route('/tasks', methods=['GET'])
@jwt_required(locations=['cookies'])
def index_html():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    # print(current_user) # this is just id
    with app.app_context():
        return render_template("tasks/index.html", current_user=user.email)
    # return "TASKS"


@tasks.route('/api/v1/tasks', methods=['GET'])
@jwt_required(locations=['cookies'])
def index():
    user_id = get_jwt_identity()
    # the_tasks = Task.query.all()
    # res = db.session.execute(select(Task.id, Task.name).where(Task.user_id == user_id).order_by(Task.id)).scalars().all()
    res = db.session.execute(select(Task.id, Task.name).where(Task.user_id == user_id).order_by(Task.id))
    # breakpoint()
    # for row in res:
    #     print(f"{row.id}  {row.name}")
    res = [dict(id=s.id, name=s.name) for s in res]
    return dict(code=0, tasks=res), 201


@tasks.route('/api/v1/tasks', methods=['POST'])
@jwt_required(locations=['cookies'])
def create():
    user_id = get_jwt_identity()
    # user = User.query.get(user_id)

    try:
        creds = TaskAttrs.parse_raw(request.data)
    except ValidationError as e:
        errors = json.loads(e.json())
        print("RegistrationCredentials", e.json())
        return dict(code=-1, msg=errors), 400

    # breakpoint()
    # creds = collections.defaultdict(creds)
    final_creds = collections.defaultdict(None)
    for key, value in creds:
        final_creds[key] = value
    print(final_creds)
    task = Task(name=final_creds['name'], desc=final_creds['desc'], user_id=user_id, parent_task_id=final_creds['parent_task_id'])
    print(task)
    db.session.add(task)
    db.session.commit()

    return dict(code=0, msg="new task has been created"), 201


class TaskAttrs(BaseModel):
    name: str
    desc: Optional[str]
    parent_task_id: Optional[int]
