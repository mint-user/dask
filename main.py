from flask import Flask, escape, request

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/api/v1/task', methods=['POST'])
"""
create new task
"""
def create_task():
    pass
# export FLASK_APP=main.py && export FLASK_ENV=development && flask run
# $ export FLASK_APP=sample
# $ export FLASK_ENV=development
# $ flask run
