from flask import Blueprint


tasks = Blueprint("tasks", __name__, static_folder="static", template_folder='templates', static_url_path='/static'
                                                                                                          '/tasks')
