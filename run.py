from app import app


def run():
    # app.run(host='localhost', port=8080)
    app.run(host=app.config.HOST, port=app.config.PORT)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080)
    # app.run(host='localhost', port=8080)
    run()
    # venv / bin / python run.py
#     poetry run python run.py
