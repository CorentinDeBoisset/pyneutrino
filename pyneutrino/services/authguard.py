from functools import wraps
from flask import session, g
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import NoResultFound
from pyneutrino.db import db, UserAccount
from typing import Callable


def authguard(handler: Callable):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            raise Unauthorized

        try:
            g.current_user = db.session.execute(db.select(UserAccount).filter_by(id=session["user_id"])).scalar_one()
        except NoResultFound:
            session.clear()
            raise Unauthorized

        return handler(*args, **kwargs)

    return wrapped
