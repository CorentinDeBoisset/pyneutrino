import os

from flask import Flask

from .db import db, migrate
from .errors import register_error_handlers
from .home import register as register_home
from .auth import register as register_auth
from .hooks import register as register_hooks


def create_app(dev=False, test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="./static",
        static_url_path="/static"
    )

    app.config.from_mapping(
        SESSION_COOKIE_SAMESITE="Strict"
    )

    if test_config is None:
        if dev:
            # Set the default configuration for the dev environment
            app.config.from_mapping(
                SECRET_KEY="secret-key",
                CSRF_TOKEN_SALT="csrf-salt",
                SQLALCHEMY_DATABASE_URI="postgresql://neutrino:neutrinopwd@127.0.0.1:5432/neutrino",
                SESSION_COOKIE_SAMESITE="Strict"
            )

        # Load a configuration file targeted with the environment: NEUTRINO_SETTING_FILE=/path/to/settings.cfg
        app.config.from_envvar('NEUTRINO_SETTING_FILE', silent=True)
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

    # First, register hooks and error handlers
    register_error_handlers(app)
    register_hooks(app)

    # Register blueprints
    register_home(app)
    register_auth(app)

    return app
