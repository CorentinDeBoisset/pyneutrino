from flask import Flask
from .xsrf import XsrfBp

# These are dummy blueprints, to register global hooks using
# the @bp.before_app_request and @bp.after_app_request decorators


def register(app: Flask):
    app.register_blueprint(XsrfBp)
