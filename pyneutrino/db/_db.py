from flask import Flask
from flask.globals import app_ctx
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class SQLAlchemy:
    def __init__(self):
        self.engine = None
        self.session = None

    @staticmethod
    def get_context_id():
        # This is a proxy, see here: https://werkzeug.palletsprojects.com/en/3.0.x/local/#proxy-objects
        return id(app_ctx._get_current_object())

    def shutdown_session(self, exception: BaseException | None = None):
        self.session.remove()

    def init_app(self, app: Flask):
        url = app.config["SQLALCHEMY_DATABASE_URI"]
        echo = app.config.get("SQLALCHEMY_ECHO", False)
        self.engine = create_engine(url, echo=echo)
        self.session = scoped_session(sessionmaker(self.engine), self.get_context_id)
        app.teardown_appcontext(self.shutdown_session)


db = SQLAlchemy()
