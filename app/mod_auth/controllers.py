from app import app, db
from app.mod_auth.models import User
from flask import request


@app.route('/')
def hello():
    user = User.query.all()
    return str(user)
    # return 'Hello, World!'


@app.route('/api/v1/accounts', methods=['POST', 'GET'])
def create_user():
    """
    create new user
    """
    print("POST REQUEST=====================")
    print(request.data)
    if not ("email" in request.json.keys() and "password" in request.json.keys()):
        return {"error": "Request should contain 'email' and 'password' fields"}, 409
    else:
        user = User.query.filter(User.email == request.json['email']).first()
        print(user)
        if user is not None:
            return {"error": "Email is already used"}, 202
        else:
            user = User(email=request.json['email'], password=request.json['password'])
            db.session.add(user)
            db.session.commit()
            return str(request.data), 201
