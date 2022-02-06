import re
import secrets

from app import app, db
from app.mod_auth.models import User
from flask import request
from flask_bcrypt import Bcrypt
from datetime import timedelta, datetime

bcrypt = Bcrypt(app)


@app.route('/')
def hello():
    user = User.query.all()
    return str(user)
    # return 'Hello, World!'


@app.route('/api/v1/accounts/<int:id>', methods=['PATCH'])
def update_user():
    print(request.data)


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
    if not bcrypt.check_password_hash(pass_hash, request.json['password']):
        return {"error": "Wrong email or password"}, 401

    # generate token
    token = secrets.token_hex(16)

    now = datetime.now()
    delta = timedelta(hours=1)
    token_expires = (now + delta)

    user.token = token
    user.token_expires = token_expires

    db.session.add(user)
    db.session.commit()
    return {"token": token, "token_expires": token_expires.strftime('%Y-%m-%d %H:%M:%S')}, 201


@app.route('/api/v1/accounts', methods=['POST'])
def create_user():
    """
    create new user
    """
    print("POST REQUEST=====================")
    print(request.data)
    # check fields
    print(request.json)
    print(request.json.keys())
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

    user = User.query.filter(User.email == email).first()
    print(user)
    if user is not None:
        return {"error": "Email is already used"}, 202

    pass_hash = bcrypt.generate_password_hash(password)
    user = User(email=email, password=pass_hash)
    db.session.add(user)
    db.session.commit()
    return str(request.data), 201
