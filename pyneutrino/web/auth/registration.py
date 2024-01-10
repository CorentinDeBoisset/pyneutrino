import secrets
from uuid import uuid4
from argon2 import PasswordHasher
from flask import Blueprint, request, jsonify
from sqlalchemy import select
from werkzeug.exceptions import Conflict
from pyneutrino.services import validate_schema
from pyneutrino.db import db, UserAccount
from datetime import datetime

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

    ph = PasswordHasher()
    password_hash = ph.hash(json_body["password"])
    verification_code_hash = ph.hash(secrets.token_urlsafe(32))

    # Check the username and email are not already reserved
    existing_email = db.session.execute(select(UserAccount).filter_by(email=json_body["email"])).scalar()
    if existing_email is not None:
        raise Conflict("registration_email_conflict")

    existing_username = db.session.execute(select(UserAccount).filter_by(username=json_body["username"])).scalar()
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
