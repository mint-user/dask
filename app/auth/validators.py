import re

from app import app
from app.auth.models import User
from pydantic import BaseModel, ValidationError, validator, root_validator

from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)


class Credentials(BaseModel):
    email: str
    password: str


class LoginCredentials(Credentials):
    @root_validator
    def user_exists(cls, values):
        email = values.get('email')
        password = values.get('password')

        user = User.query.filter(User.email == email).first()
        if user is None:
            raise ValueError("Wrong email or password")

        # check password
        pass_hash = user.password
        print("CHECKING PASSWORD!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        if not bcrypt.check_password_hash(pass_hash, password):
            raise ValueError("Wrong email or password")

        return dict(user=user)


# class AuthError(ValueError):
#     def __init__(self, message, code=400):
#         self.message = message
#         self.code = code
#         super().__init__(self.message, self.code)


class RegistrationCredentials(Credentials):
    @validator('email')
    def email_should_contain_dog(cls, email):
        if "@" not in email:
            raise ValueError("Email must contain '@'")
            # raise AuthError("Email must contain '@", 406)

        return email

    @validator('email')
    def email_not_registered(cls, email):
        user = User.query.filter(User.email == email).first()
        print(user)
        if user is not None:
            raise ValueError("Email is already used")

        return email

    @validator('password')
    def password_should_be_strong(cls, password):
        if 20 <= len(password) or len(password) <= 8:
            raise ValueError("Password should contain 8..20 characters")

        if re.search("[a-z]", password) is None:
            raise ValueError("Password should contain lowercase letters")

        if re.search("[A-Z]", password) is None:
            raise ValueError("Password should contain uppercase letters")

        if re.search("\d", password) is None:
            raise ValueError("Password should contain digits")

        return password