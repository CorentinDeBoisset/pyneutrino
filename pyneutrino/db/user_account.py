from datetime import datetime
from sqlalchemy import String, Uuid, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from ._db import db


# known bug: https://github.com/python/mypy/issues/8603
class UserAccount(db.Model):  # type: ignore[name-defined]
    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    public_key: Mapped[str] = mapped_column(String, nullable=False)
    private_key: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True)
    creation_date: Mapped[datetime] = mapped_column(DateTime)
    password_hash: Mapped[str] = mapped_column(String)
    email_verification_code: Mapped[str] = mapped_column(String)
    email_verification_date: Mapped[datetime] = mapped_column(DateTime)
