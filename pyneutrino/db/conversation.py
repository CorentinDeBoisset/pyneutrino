from sqlalchemy import String, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._db import db


# known bug: https://github.com/python/mypy/issues/8603
class Conversation(db.Model):  # type: ignore[name-defined]
    id: Mapped[int] = mapped_column(Uuid, primary_key=True)
    creator: Mapped[str] = mapped_column(Uuid, ForeignKey("user_account.id"))

    # We either have an account liked to the receiver, or an anonymous receiver where we only save the public key
    receiver: Mapped[str] = mapped_column(Uuid, ForeignKey("user_account.id"), nullable=True)
    reveiver_public_key: Mapped[str] = mapped_column(String, nullable=True)
