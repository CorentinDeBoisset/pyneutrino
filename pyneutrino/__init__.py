import os
import errno
import yaml
import json
from flask import Flask

from .db import db, redis
from .hooks import register as register_hooks
from .commands import register as register_commands
from .web.home import register as register_home
from .web.error_management import register_error_handlers
from .web.auth import register as register_auth
from .web.messaging import register as register_messaging


def get_config():
    config = {
        "SESSION_COOKIE_SAMESITE": "Strict",
        "SECRET_KEY": "secret-key",
        "CSRF_TOKEN_SALT": "csrf-salt",
        "SQLALCHEMY_DATABASE_URI": "postgresql://neutrino:neutrinopwd@127.0.0.1:5432/neutrino",
        "REDIS_URI": "redis://localhost:6379",
    }

    config_file = os.environ.get("NEUTRINO_SETTING_FILE", default="")
    if config_file:
        try:
            with open(config_file, mode="rb") as config_file_contents:
                # Read as JSON or YANL
                if config_file.endswith(".yaml") or config_file.endswith(".yml"):
                    loaded_configuration = yaml.safe_load(config_file_contents)
                elif config_file.endswith(".json"):
                    loaded_configuration = json.load(config_file_contents)
                else:
                    raise Exception("Unsuppported configuration file (only .json, .yml or .yaml are supported)")

                if isinstance(loaded_configuration, dict):
                    config.update(loaded_configuration)
        except OSError as e:
            if e.errno in (errno.ENOENT, errno.EISDIR, errno.ENOTDIR):
                return False
            e.strerror = f"Unable to load configuration file ({e.strerror})"
            raise

    return config


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder="./static", static_url_path="/static")

    app.config.from_mapping(**get_config())

    if test_config is None:
        # Load a configuration file targeted with the environment: NEUTRINO_SETTING_FILE=/path/to/settings.cfg
        app.config.from_envvar("NEUTRINO_SETTING_FILE", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)
    redis.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # First, register hooks and error handlers
    register_error_handlers(app)
    register_hooks(app)
    register_commands(app)

    # Register blueprints
    register_home(app)
    register_auth(app)
    register_messaging(app)

    return app
