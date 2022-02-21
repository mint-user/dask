from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dynaconf import FlaskDynaconf

app = Flask(__name__)
app.config.from_object('config')
FlaskDynaconf(app, settings_files=["settings.toml"])
db = SQLAlchemy(app)

print("Dynaconf var: a_boolean =", app.config.a_boolean)

from .auth.routes import auth

app.register_blueprint(auth)
