from flask import Flask
from .wait_db import WaitDbBp


def register(app: Flask):
    app.register_blueprint(WaitDbBp)
