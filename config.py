import os
from datetime import timedelta

DEBUG = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'example.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# JWT
JWT_SECRET_KEY = "super-secret"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
# JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=40)
# JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=2)
