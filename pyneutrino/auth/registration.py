import secrets
from passlib.hash import argon2
from flask import Blueprint, request, jsonify
from pyneutrino.services.jsonschema import validate_schema
from pyneutrino.db import db, UserAccount
from datetime import datetime
from uuid import uuid4

RegistrationBp = Blueprint('registration', __name__, url_prefix="/api/register")


new_account_schema = {
    "required": ["email", "username", "password", "public_key", "private_key"],
    "properties": {
        "email": {"type": "string", "pattern": "^\\S+@\\S+\\.\\S+$"},
        "username": {"type": "string"},
        "password": {"type": "string"},
        "public_key": {"type": "string"},
        "private_key": {"type": "string"},
    }
}


@RegistrationBp.route("/new-account", methods=["POST"])
@validate_schema(new_account_schema)
def new_account():
    json_body = request.get_json()

    # TODO: check password strength, validate private and public key format

    password_hash = argon2.hash(json_body["password"])
    verification_code_hash = argon2.hash(secrets.token_urlsafe(32))

    new_user = UserAccount(
        id=uuid4(),
        username=json_body["username"],
        email=json_body["email"],
        public_key=json_body["public_key"],
        private_key=json_body["private_key"],
        creation_date=datetime.now(),
        password_hash=password_hash,
        email_verification_code=verification_code_hash
    )
    db.session.add(new_user)
    db.session.commit()

    # TODO: manage errors when saving in the database

    return jsonify(message="Ok"), 201


validate_account_schema = {
    "required": ["email", "validation_code"],
    "properties": {
        "email": {"type": "string"},
        "validation_code": {"type": "string"},
    }
}


@RegistrationBp.route("/validate-account", methods=["POST"])
@validate_schema(validate_account_schema)
def validate_account():
    return "TODO"
