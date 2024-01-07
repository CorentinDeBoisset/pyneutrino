from flask import Flask
from .conversation import ConversationBp
from .messages import MessagesBp


def register(app: Flask):
    app.register_blueprint(ConversationBp)
    app.register_blueprint(MessagesBp)
