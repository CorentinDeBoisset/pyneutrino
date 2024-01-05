from flask import Flask
from .conversation import ConversationBp


def register(app: Flask):
    app.register_blueprint(ConversationBp)
