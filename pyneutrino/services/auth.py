from uuid import uuid4
from functools import wraps
from typing import Callable
from flask import session, g
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from pyneutrino.db import db, UserAccount


def authguard(handler: Callable):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            raise Unauthorized

        try:
            g.current_user = db.session.execute(select(UserAccount).filter_by(id=session["user_id"])).scalar_one()
        except NoResultFound:
            session.clear()
            raise Unauthorized

        return handler(*args, **kwargs)

    return wrapped


def login_user(user: UserAccount):
    # Flask stores the session data in a cookie so be careful not to put any sensitive data in there
    session["user_id"] = user.id
    session["session_id"] = str(uuid4())
    # If user roles are implemented, store it in the session to add a firewall on the routes
