from app import app
from flask import request
from app import db
from app.mod_auth.models import User

db.create_all()


@app.route('/')
def hello():
    user = User.query.all()
    return str(user)
    # return 'Hello, World!'


@app.route('/api/v1/accounts', methods=['POST'])
def create_user():
    """
    create new user
    """
