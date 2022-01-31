from app import app, db
from app.mod_auth.models import User
from flask import request


@app.route('/')
def hello():
    user = User.query.all()
    return str(user)
    # return 'Hello, World!'


@app.route('/api/v1/accounts/<int:id>', methods=['PATCH'])
def update_user():
    print(request.data)


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
            user = User(email=email, password=request.json['password'])
            db.session.add(user)
            db.session.commit()
            return str(request.data), 201
