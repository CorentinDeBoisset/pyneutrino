import os

from flask import Flask

from .db import db, migrate
from .errors import register_error_handlers
from .home import register as register_home
from .auth import register as register_auth
# from .chat import register as register_chat

def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="./static",
        static_url_path="/static"
    )

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="postgresql://neutrino:neutrinopwd@127.0.0.1:5432/neutrino",
        SESSION_COOKIE_SAMESITE="Strict"
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    register_home(app)
    register_auth(app)
    # register_chat(app)
    register_error_handlers(app)

    return app
