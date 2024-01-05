from flask import Flask
from .session import SessionBp
from .registration import RegistrationBp


def register(app: Flask):
    app.register_blueprint(SessionBp)
    app.register_blueprint(RegistrationBp)
