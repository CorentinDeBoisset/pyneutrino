import secrets
from passlib.hash import argon2
from flask import Blueprint, request, jsonify
from pyneutrino.services import validate_schema
from pyneutrino.db import db, UserAccount
from datetime import datetime
from uuid import uuid4
from werkzeug.exceptions import Conflict

RegistrationBp = Blueprint("registration", __name__, url_prefix="/api/auth/register")


new_account_schema = {
    "required": ["email", "username", "password", "public_key", "private_key"],
    "properties": {
        "email": {"type": "string", "pattern": "^\\S+@\\S+\\.\\S+$"},
        "username": {"type": "string", "minLength": 6},
        "password": {"type": "string", "minLength": 4},
        "public_key": {"type": "string"},
        "private_key": {"type": "string"},
    },
}


@RegistrationBp.route("/new-account", methods=["POST"])
@validate_schema(new_account_schema)
def new_account():
    json_body = request.get_json()

    # TODO: check password strength, validate private and public key format

    password_hash = argon2.hash(json_body["password"])
    verification_code_hash = argon2.hash(secrets.token_urlsafe(32))

    # Check the username and email are not already reserved
    existing_email = db.session.execute(db.select(UserAccount).filter_by(email=json_body["email"])).scalar()
    if existing_email is not None:
        raise Conflict("registration_email_conflict")

    existing_username = db.session.execute(db.select(UserAccount).filter_by(username=json_body["username"])).scalar()
    if existing_username is not None:
        raise Conflict("registration_username_conflict")

    new_user = UserAccount(
        id=uuid4(),
        username=json_body["username"],
        email=json_body["email"],
        public_key=json_body["public_key"],
        private_key=json_body["private_key"],
        creation_date=datetime.now(),
        password_hash=password_hash,
        email_verification_code=verification_code_hash,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="Ok"), 201


new_anonymous_account_schema = {
    "required": ["public_key"],
    "properties": {
        "public_key": {"type": "string"},
    },
}


@RegistrationBp.route("/new-anonymous-account", methods=["POST"])
@validate_schema(new_account_schema)
def new_anonymous_account():
    json_body = request.get_json()

    # We don't define a password, the user won't be able to login again
    # TODO: add a cleanup task to purge old anonymous users

    new_user = UserAccount(
        id=uuid4(),
        public_key=json_body["public_key"],
        creation_date=datetime.now(),
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="Ok"), 201


validate_account_schema = {
    "required": ["email", "validation_code"],
    "properties": {
        "email": {"type": "string"},
        "validation_code": {"type": "string"},
    },
}


@RegistrationBp.route("/validate-account", methods=["POST"])
@validate_schema(validate_account_schema)
def validate_account():
    return "TODO"
