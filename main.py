from flask import Flask, escape, request
from flask_sqlalchemy import SQLAlchemy
# from models import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    token = db.Column(db.String)
    token_expires = db.Column(db.DateTime)

    def __repr__(self):
        return "<User %r>" % self.email


db.create_all()
# db.session.add(User(email="qwe@dask.ru", password="f43reпg54yehw32SGD"))
# db.session.commit()

user = User.query.all()
print(user)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/api/v1/accounts', methods=['POST'])
def create_user():
    """
    create new user
    """

# export FLASK_APP=main.py && export FLASK_ENV=development && flask run
# $ export FLASK_APP=sample
# $ export FLASK_ENV=development
# $ flask run
