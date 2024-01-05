from datetime import datetime
from sqlalchemy import Text, String, Uuid, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from ._db import db


# known bug: https://github.com/python/mypy/issues/8603
class UserAccount(db.Model):  # type: ignore[name-defined]
    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    public_key: Mapped[str] = mapped_column(Text)
    private_key: Mapped[str] = mapped_column(Text)
    creation_date: Mapped[datetime] = mapped_column(DateTime)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=True)
    email_verification_code: Mapped[str] = mapped_column(String, nullable=True)
    email_verification_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # We override repr to avoid leaking hashes in logs or errors
    def __repr__(self):
        viewable_dict = {k: v for (k, v) in self.__dict__.items()}
        viewable_dict["password_hash"] = "CENSORED"
        viewable_dict["email_verification_code"] = "CENSORED"

        return f"{self.__class__}({repr(viewable_dict)})"
