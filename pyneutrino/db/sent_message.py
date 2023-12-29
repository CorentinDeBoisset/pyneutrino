from datetime import datetime
from sqlalchemy import DateTime, String, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._db import db


# known bug: https://github.com/python/mypy/issues/8603
class SentMessage(db.Model):  # type: ignore[name-defined]
    id: Mapped[int] = mapped_column(Uuid, primary_key=True)
    conversation: Mapped[str] = mapped_column(Uuid, ForeignKey("conversation.id"))
    sender: Mapped[str] = mapped_column(Uuid, ForeignKey("user_account.id"))
    creation_date: Mapped[datetime] = mapped_column(DateTime)
    message: Mapped[int] = mapped_column(String, nullable=True)
