from flask import Blueprint, request, session, jsonify
from argon2 import PasswordHasher
from pyneutrino.services import validate_schema
from pyneutrino.db import db, UserAccount
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from uuid import uuid4

SessionBp = Blueprint("auth", __name__, url_prefix="/api/auth/session")


login_schema = {
    "required": ["email", "password"],
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
}


@SessionBp.route("/login", methods=["POST"])
@validate_schema(login_schema)
def login():
    json_body = request.get_json()

    # In the future, maybe replace the authentication method with SRP:
    # https://pythonhosted.org/srp/srp.html#usage

    try:
        user = db.session.execute(select(UserAccount).filter_by(email=json_body["email"])).scalar_one()
    except NoResultFound:
        session.clear()
        raise Unauthorized()

    # If the user is already logged in, we log them out first, then succeed
    if (not session.new) and ("user_id" in session) and (session["user_id"] != user.id):
        session.clear()

    ph = PasswordHasher
    if not ph.verify(user.password_hash, json_body["password"]):
        session.clear()
        raise Unauthorized()

    # Flask stores the session data in a cookie so be careful not to put any sensitive data in there
    session["user_id"] = user.id
    session["session_id"] = str(uuid4())

    # If user roles are implemented, store it in the session to add a firewall on the routes

    return jsonify(
        id=user.id,
        email=user.email,
        username=user.username,
        public_key=user.public_key,
        private_key=user.private_key,
        creation_date=user.creation_date,
        email_verification_date=user.email_verification_date,
    )


@SessionBp.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return "", 204
