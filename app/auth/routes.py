import json
from flask_jwt_extended import create_access_token, JWTManager, set_access_cookies, unset_jwt_cookies, jwt_required, \
    get_jwt, create_refresh_token, set_refresh_cookies, get_jwt_identity

from app import app
from app.auth import auth
from app.auth.models import User, db
from flask import request, jsonify, render_template
from flask_bcrypt import Bcrypt
from pydantic import ValidationError

from app.auth.validators import RegistrationCredentials, Credentials, LoginCredentials


bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# @jwt_required(locations=['cookies'])
# def render_index(request):
#     current_user = get_jwt_identity()


@auth.route('/', methods=['GET'])
def index():
    # if "access_token" in request.cookies.keys():
    #     render_index(request)
    # else:
    with app.app_context():
        return render_template("auth/login.html")


# update account
@auth.route('/api/v1/accounts', methods=['PATCH'])
@jwt_required(locations=['cookies'])
def update_user():
    print("update REQUEST", request.data)

    # check fields
    try:
        creds = RegistrationCredentials.parse_raw(request.data)
    except ValidationError as e:
        errors = json.loads(e.json())
        print(e)
        return dict(code=-1, msg=errors), 400

    user_id = get_jwt()["sub"]
    user = User.query.filter(User.id == user_id).first()

    email = creds.email
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
@auth.route('/api/v1/accounts/session', methods=['DELETE'])
@jwt_required(locations=['cookies'])
def logout():
    print(request.data)

    resp = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(resp)
    return resp


# login
@auth.route('/api/v1/accounts/session', methods=['POST'])
def login():
    print("LOGIN REQUEST", request.data)

    try:
        creds = Credentials.parse_raw(request.data)
        user = LoginCredentials(email=creds.email, password=creds.password).user
    except ValidationError as e:
        errors = json.loads(e.json())
        print(e)
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

    # check fields
    try:
        creds = RegistrationCredentials.parse_raw(request.data)
    except ValidationError as e:
        errors = json.loads(e.json())
        print(e)
        return dict(code=-1, msg=errors), 400

    email = creds.email
    password = creds.password

    pass_hash = bcrypt.generate_password_hash(password)
    user = User(email=email, password=pass_hash)
    db.session.add(user)
    db.session.commit()

    resp = jsonify({"msg": "registration successful"})
    return resp, 201
