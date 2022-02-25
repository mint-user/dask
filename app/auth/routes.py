import json
from flask_jwt_extended import create_access_token, JWTManager, set_access_cookies, unset_jwt_cookies, jwt_required, \
    get_jwt, create_refresh_token, set_refresh_cookies, get_jwt_identity, verify_jwt_in_request
from jwt import ExpiredSignatureError
from werkzeug.utils import redirect

from app import app
from app.auth import auth
from app.auth.models import User, db
from flask import request, jsonify, render_template, make_response
from flask_bcrypt import Bcrypt
from pydantic import ValidationError

from app.auth.validators import RegistrationCredentials, Credentials, LoginCredentials

bcrypt = Bcrypt(app)
jwt = JWTManager(app)


def _email_is_free(email, user_id=None):
    user = User.query.filter(User.email == email).first()
    print(user)
    if user_id is None:  # register
        if user is not None:
            # breakpoint()
            raise ValueError("Email is already used")
    else:  # update
        if (user is not None) and user.id != user_id:
            raise ValueError("Email is already used")

# @jwt_required(locations=['cookies'])
# def render_index(request):


@auth.route('/', methods=['GET'])
def index():
    try:
        # breakpoint()
        verify_jwt_in_request(locations=['cookies'])
        resp = make_response(redirect('/tasks'))
        return resp
    except:
        # resp = make_response(redirect('/login'))
        # unset_jwt_cookies(resp)
        # return resp
        with app.app_context():
            return render_template("auth/login.html")




# @auth.route('/login', methods=['GET'])
# def login_page():
#     with app.app_context():
#         return render_template("auth/login.html")


# update account
@auth.route('/api/v1/accounts', methods=['PATCH'])
@jwt_required(locations=['cookies'])
def update_user():
    print("update REQUEST", request.data)

    # check fields
    user_id = get_jwt_identity()
    # obj_to_parse = json.loads(request.data)
    # obj_to_parse["user_id"] = user_id
    # obj_to_parse = json.dumps(obj_to_parse)
    try:
        creds = RegistrationCredentials.parse_raw(request.data)
        # breakpoint()
    except ValidationError as e:
        errors = json.loads(e.json())
        print(e)
        return dict(code=-1, msg=errors), 400

    user_id = get_jwt()["sub"]
    email = creds.email
    try:
        _email_is_free(email, user_id=user_id)
    except ValueError as e:
        return dict(code=-1, msg=[{"loc": ["email"], "msg": str(e), "type": "value_error"}]), 400

    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return dict(code=-1, msg=[{"loc": ["email"], "msg": "User is deleted", "type": "value_error"}]), 400

    password = creds.password

    pass_hash = bcrypt.generate_password_hash(password)
    user.email = email
    user.password = pass_hash

    db.session.add(user)
    db.session.commit()

    # resp = jsonify({"msg": "successful update"})
    resp = jsonify(code=0, msg="Successful update", email=user.email)
    return resp


# refresh
@auth.route('/api/v1/accounts/session/refresh', methods=['PATCH'])
@jwt_required(refresh=True, locations=['cookies'])
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the JWT access cookie in the response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


# logout
@auth.route('/api/v1/accounts/logout', methods=['GET'])
def logout():
    # print(request.data)
    response = make_response(redirect('/'))
    try:
        # verify_jwt_in_request(optional=True, locations=['cookies'])
        unset_jwt_cookies(response)
    except ExpiredSignatureError:
        pass
    finally:
        return response





# login
@auth.route('/api/v1/accounts/session', methods=['POST'])
def login():
    print("LOGIN REQUEST", request.data)

    try:
        creds = Credentials.parse_raw(request.data)
        user = LoginCredentials(email=creds.email, password=creds.password).user
    except ValidationError as e:
        errors = json.loads(e.json())
        print("LOGIN error", e)
        return dict(code=-1, msg=errors), 400

    resp = jsonify(code=0, msg="Successful login", email=user.email)
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp


# register
@auth.route('/api/v1/accounts', methods=['POST'])
def create_user():
    """
    create new user
    {"email": "qwe@qwe", "password": "oIwi5jdPJlLGzba"}
    """
    print("REQUEST create user ", request.data)

    # validate fields
    try:
        creds = RegistrationCredentials.parse_raw(request.data)
    except ValidationError as e:
        errors = json.loads(e.json())
        print("RegistrationCredentials", e.json())
        return dict(code=-1, msg=errors), 400

    # email is not registered
    email = creds.email
    # user = User.query.filter(User.email == email).first()
    # print(user)
    # if user is not None:
    #     return dict(code=-1, msg=[{"loc": ["email"], "msg": "Email is already used", "type": "value_error"}]), 400
    try:
        _email_is_free(email, user_id=None)
        # breakpoint()
    except ValueError as e:
        # breakpoint()
        return dict(code=-1, msg=[{"loc": ["email"], "msg": str(e), "type": "value_error"}]), 400

    password = creds.password
    pass_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(email=email, password=pass_hash)
    db.session.add(user)
    db.session.commit()
    # breakpoint()

    # resp = jsonify({"msg": "registration successful"})
    # return resp, 201
    return dict(code=0, msg="registration successful"), 201



