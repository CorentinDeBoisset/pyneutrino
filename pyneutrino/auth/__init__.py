from flask import Flask
from .login import LoginBp


def register(app: Flask):
    app.register_blueprint(LoginBp)
