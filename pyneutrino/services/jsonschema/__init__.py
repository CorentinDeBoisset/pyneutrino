from functools import wraps
from flask import request, current_app
from werkzeug.exceptions import BadRequest, InternalServerError
from jsonschema import validate, ValidationError, SchemaError
from typing import Callable


def validate_schema(schema: dict):
    def decorator(handler: Callable):
        @wraps(handler)
        def wrapped(*args, **kwargs):
            request_body = request.get_json()
            try:
                validate(instance=request_body, schema=schema)
            except SchemaError as e:
                current_app.logger.error(f"Invalid json schema: {e.message}")
                raise InternalServerError
            except ValidationError as e:
                raise BadRequest(f"Invalid json: {e.message}")

            return handler(*args, **kwargs)

        return wrapped

    return decorator
