import re
import secrets

from flask_jwt_extended import create_access_token, JWTManager, set_access_cookies, unset_jwt_cookies, jwt_required, \
    get_jwt

from app import app, db
from app.mod_auth.models import User
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from datetime import timedelta, datetime

bcrypt = Bcrypt(app)
jwt = JWTManager(app)


@app.route('/')
def hello():
    user = User.query.all()
    return str(user)
    # return 'Hello, World!'


# update account
@app.route('/api/v1/accounts', methods=['PATCH'])
@jwt_required()
def update_user():
    print(request.data)
    user_id = get_jwt()["sub"]
    user = User.query.filter(User.id == user_id).first()

    if request.json is None:
        return {"msg": "wrong attributes"}, 400

    if not ("email" in request.json.keys() or "password" in request.json.keys()):
        return {"msg": "wrong attributes"}, 400

    if "email" in request.json.keys():
        user.email = request.json['email']

    if "password" in request.json.keys():
        pass_hash = bcrypt.generate_password_hash(request.json['password'])
        user.password = pass_hash

    db.session.add(user)
    db.session.commit()

    resp = jsonify({"msg": "successful update"})
    return resp


# logout
@app.route('/api/v1/accounts/session', methods=['DELETE'])
def logout():
    print(request.data)

    resp = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(resp)
    return resp


# login
@app.route('/api/v1/accounts/session', methods=['POST'])
def login():
    print(request.data)
    # check request structure
    if 'email' not in request.json.keys() or 'password' not in request.json.keys():
        return {"error": "Bad request"}, 400

    # email exists
    email = request.json['email']
    user = User.query.filter(User.email == email).first()
    if user is None:
        return {"error": "Wrong email or password"}, 401

    # check password
    pass_hash = user.password
    print("CHECKING PASSWORD!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if not bcrypt.check_password_hash(pass_hash, request.json['password']):
        return {"error": "Wrong email or password"}, 401

    response = jsonify({"msg": "login successful"})
    access_token = create_access_token(identity=user.id)
    set_access_cookies(response, access_token)
    return response


# register
@app.route('/api/v1/accounts', methods=['POST'])
def create_user():
    """
    create new user
    """
    print("POST REQUEST=====================")
    print(request.data)
    # check fields
    if not ("email" in request.json.keys() and "password" in request.json.keys()):
        return {"error": "Request should contain 'email' and 'password' fields"}, 400

    # check email is correct
    email = request.json['email']
    if "@" not in email:
        return {"error": "Email should contain '@'"}, 400

    # check password
    password = request.json['password']
    if 20 <= len(password) or len(password) <= 8:
        return {"error": "Password should contain 8..20 characters"}, 400

    if re.search("[a-z]", password) is None:
        return {"error": "Password should contain lowercase letters"}, 400

    if re.search("[A-Z]", password) is None:
        return {"error": "Password should contain uppercase letters"}, 400

    if re.search("\d", password) is None:
        return {"error": "Password should contain digits"}, 400

    # check email is not used
    user = User.query.filter(User.email == email).first()
    print(user)
    if user is not None:
        return {"error": "Email is already used"}, 202

    pass_hash = bcrypt.generate_password_hash(password)
    user = User(email=email, password=pass_hash)
    db.session.add(user)
    db.session.commit()
    # access_token = create_access_token(identity=user.id)
    # return {"access_token": access_token}, 201
    resp = jsonify({"msg": "registration successful"})
    access_token = create_access_token(identity=user.id)
    set_access_cookies(resp, access_token)
    return resp
