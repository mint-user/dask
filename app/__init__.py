from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dynaconf import FlaskDynaconf


app = Flask(__name__)
app.config.from_object('config')
FlaskDynaconf(app, settings_files=["settings.toml"])
db = SQLAlchemy(app)

print("Dynaconf var: a_boolean =", app.config.a_boolean)

from .tasks.routes import tasks
app.register_blueprint(tasks)

from .auth.routes import auth
app.register_blueprint(auth)




db.create_all()