import collections
import json
from datetime import datetime, timezone, timedelta
from typing import Optional

from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, get_jwt, create_access_token, \
    set_access_cookies, verify_jwt_in_request, unset_jwt_cookies
from flask_jwt_extended.exceptions import NoAuthorizationError
from jinja2 import Markup
from jwt import ExpiredSignatureError
from pydantic import BaseModel, ValidationError, validator
from sqlalchemy import select
from werkzeug.utils import redirect

from app import app, db
from app.auth.models import User
from app.tasks.models import Task
from app.tasks import tasks

from flask import request, jsonify, render_template, make_response, render_template_string

jwt = JWTManager(app)


@tasks.after_request
# @tasks.before_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(seconds=20))
        print(target_timestamp - exp_timestamp)
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify(code="dave", err="I can't let you do that"), 401


@tasks.route('/tasks', methods=['GET'])
def index_html():
    # check access token
    try:
        # verify_jwt_in_request(optional=True, locations=['cookies'])
        # breakpoint()
        verify_jwt_in_request(locations=['cookies'])
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        assert user is not None
        with app.app_context():
            return render_template("tasks/index.html", current_user=user.email)
    except (ExpiredSignatureError, NoAuthorizationError, AssertionError):
    # if not get_jwt()['fresh']:
        response = make_response(redirect('/'))
        unset_jwt_cookies(response)
        return response


@tasks.route('/api/v1/tasks', methods=['DELETE'])
@jwt_required(locations=['cookies'])
def delete_task():
    print("DELETE request", request.data)
    jwt_user_id = get_jwt_identity()

    try:
        task_id = TaskDB.parse_raw(request.data).id
    except ValidationError as e:
        errors = json.loads(e.json())
        print("TaskDB", e.json())
        return dict(code=-1, msg=errors), 400

    the_task = Task.query.filter(Task.id == task_id).first()

    # check user is owner
    if the_task.user.id != jwt_user_id:
        return dict(code=-1, msg="this is not your task"), 400
    db.session.delete(the_task)
    db.session.commit()
    return dict(code=0), 200


@tasks.route('/api/v1/tasks', methods=['GET'])
@jwt_required(locations=['cookies'])
def index():
    user_id = get_jwt_identity()
    # the_tasks = Task.query.all()
    res = db.session.execute(select(Task.id, Task.name).where(Task.user_id == user_id).order_by(Task.id))
    # for row in res:
    #     print(f"{row.id}  {row.name}")
    # res = [dict(id=s.id, name=s.name) for s in res]
    res = [dict(id=s.id, name=Markup(s.name).striptags()) for s in res]

    return jsonify(code=0, tasks=res), 200


@tasks.route('/api/v1/tasks', methods=['POST'])
@jwt_required(locations=['cookies'])
def create():
    print("CREATE request", request.data)
    user_id = get_jwt_identity()
    # user = User.query.get(user_id)

    try:
        creds = TaskAttrs.parse_raw(request.data)
    except ValidationError as e:
        errors = json.loads(e.json())
        print("TaskAttrs", e.json())
        return dict(code=-1, msg=errors), 400

    # breakpoint()
    # creds = collections.defaultdict(creds)
    final_creds = collections.defaultdict(None)
    for key, value in creds:
        final_creds[key] = None if value is None else value.strip()
    print(final_creds)
    task = Task(name=final_creds['name'], desc=final_creds['desc'], user_id=user_id,
                parent_task_id=final_creds['parent_task_id'])
    print(task)
    db.session.add(task)
    db.session.commit()

    return dict(code=0, msg="new task has been created"), 201


class TaskDB(BaseModel):
    id: int


class TaskAttrs(BaseModel):
    name: str
    desc: Optional[str]
    parent_task_id: Optional[int]

    @validator("name")
    def not_empty(cls, name):
        print("inside NAME validtor")
        if len(name.strip()) == 0:
            raise ValueError("Task name should not be empty")
            # pass
        return name
