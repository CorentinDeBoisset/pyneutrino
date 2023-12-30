from flask import Flask
from .login import LoginBp
from .registration import RegistrationBp


def register(app: Flask):
    app.register_blueprint(LoginBp)
    app.register_blueprint(RegistrationBp)
