from flask import Blueprint, request, session
from argon2 import PasswordHasher
from pyneutrino.services import validate_schema, login_user, serialize, authguard
from pyneutrino.db import db, UserAccount
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select

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
def login_route():
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

    try:
        ph = PasswordHasher()
        # If the password is not valid, argon2 raises an exception
        ph.verify(user.password_hash, json_body["password"])
    except BaseException:
        # TODO: improve logging if the hash or another error occurs
        session.clear()
        raise Unauthorized()

    login_user(user)

    return serialize(
        user, ["id", "email", "username", "public_key", "private_key", "creation_date", "email_verification_date"]
    )


@SessionBp.route("/logout", methods=["POST"])
@authguard
def logout_route():
    session.clear()

    return "", 204
