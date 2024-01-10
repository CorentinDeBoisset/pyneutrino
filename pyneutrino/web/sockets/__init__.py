from flask_socketio import SocketIO
from .messages import MessagesNamespace


def register_sockets(app: SocketIO):
    app.on_namespace(MessagesNamespace("/socket"))
