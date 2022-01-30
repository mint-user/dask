from flask import Flask, escape, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/api/v1/task', methods=['POST'])
def create_task():
    """
create new task
"""
# export FLASK_APP=main.py && export FLASK_ENV=development && flask run
# $ export FLASK_APP=sample
# $ export FLASK_ENV=development
# $ flask run
