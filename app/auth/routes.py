import json
import re
from flask_jwt_extended import create_access_token, JWTManager, set_access_cookies, unset_jwt_cookies, jwt_required, \
    get_jwt, create_refresh_token, set_refresh_cookies, get_jwt_identity

from app import app
from app.auth.models import User, db
from flask import request, jsonify, Blueprint, render_template
from flask_bcrypt import Bcrypt
from pydantic import BaseModel, ValidationError, validator, root_validator

auth = Blueprint("auth", __name__, static_folder="static", template_folder='templates', static_url_path='/static/auth')

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

    resp = jsonify({"msg": "successful update"})
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


class Credentials(BaseModel):
    email: str
    password: str


class LoginCredentials(Credentials):
    @root_validator
    def email_registered(cls, values):
        email = values.get('email')
        password = values.get('password')

        user = User.query.filter(User.email == email).first()
        if user is None:
            raise ValueError("Wrong email or password")

        # check password
        pass_hash = user.password
        print("CHECKING PASSWORD!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        if not bcrypt.check_password_hash(pass_hash, password):
            raise ValueError("Wrong email or password")

        return dict(user=user)


class RegistrationCredentials(Credentials):
    @validator('email')
    def email_should_contain_dog(cls, email):
        if "@" not in email:
            raise ValueError("Email must contain '@")

        return email

    @validator('email')
    def email_not_registered(cls, email):
        user = User.query.filter(User.email == email).first()
        print(user)
        if user is not None:
            raise ValueError("Email is already used")

        return email

    @validator('password')
    def password_should_be_strong(cls, password):
        if 20 <= len(password) or len(password) <= 8:
            raise ValueError("Password should contain 8..20 characters")

        if re.search("[a-z]", password) is None:
            raise ValueError("Password should contain lowercase letters")

        if re.search("[A-Z]", password) is None:
            raise ValueError("Password should contain uppercase letters")

        if re.search("\d", password) is None:
            raise ValueError("Password should contain digits")

        return password


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
