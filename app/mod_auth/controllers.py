import secrets

from app import app, db
from app.mod_auth.models import User
from flask import request
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)


@app.route('/')
def hello():
    user = User.query.all()
    return str(user)
    # return 'Hello, World!'


@app.route('/api/v1/accounts/<int:id>', methods=['PATCH'])
def update_user():
    print(request.data)


@app.route('/api/v1/login', methods=['POST'])
def login():
    # email exists
    print(request.data)
    email = request.json['email']
    user = User.query.filter(User.email == email).first()
    if user is None:
        return {"error": "Wrong email or password"}, 202
    else:
        pass_hash = user.password
        if bcrypt.check_password_hash(pass_hash, request.json['password']):
            token = secrets.token_hex(16)
            user.token = token
            #
            return str(request.data), 201


@app.route('/api/v1/accounts', methods=['POST'])
def create_user():
    """
    create new user
    """
    print("POST REQUEST=====================")
    print(request.data)
    if not ("email" in request.json.keys() and "password" in request.json.keys()):
        return {"error": "Request should contain 'email' and 'password' fields"}, 409
    else:
        email = request.json['email']
        user = User.query.filter(User.email == email).first()
        print(user)
        if user is not None:
            return {"error": "Email is already used"}, 202
        else:
            pass_hash = bcrypt.generate_password_hash(request.json['password'])
            user = User(email=email, password=pass_hash)
            db.session.add(user)
            db.session.commit()
            return str(request.data), 201
