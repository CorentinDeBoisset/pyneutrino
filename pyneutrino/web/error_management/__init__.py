import sys
from flask import Flask, jsonify, current_app
from werkzeug.exceptions import HTTPException, InternalServerError


def exception_to_json(e: Exception):
    if isinstance(e, HTTPException):
        if isinstance(e, InternalServerError):
            current_app.log_exception(sys.exc_info())

        return jsonify(code=e.code, name=e.name, description=e.description), e.code

    current_app.log_exception(sys.exc_info())
    return jsonify(code=500, name="Internal server error", description=InternalServerError.description), 500


def register_error_handlers(app: Flask):
    app.register_error_handler(Exception, exception_to_json)
