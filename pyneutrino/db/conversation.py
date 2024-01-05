from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import Text, Uuid, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from ._db import db

if TYPE_CHECKING:
    from .sent_message import SentMessage
    from .user_account import UserAccount


# known bug: https://github.com/python/mypy/issues/8603
class Conversation(db.Model):  # type: ignore[name-defined]
    id: Mapped[int] = mapped_column(Uuid, primary_key=True)
    creator_id: Mapped[str] = mapped_column(
        Uuid,
        ForeignKey("user_account.id", name="created_conversations_fkey"),
    )
    creator: Mapped["UserAccount"] = db.relationship(
        back_populates="created_conversations",
        foreign_keys=[creator_id]
    )

    # We either have an account liked to the receiver, or an anonymous receiver where we only save the public key
    receiver_id: Mapped[str] = mapped_column(
        Uuid,
        ForeignKey("user_account.id", name="received_conversation_fkey"),
        nullable=True,
    )
    receiver: Mapped["UserAccount"] = db.relationship(
        back_populates='received_conversations',
        foreign_keys=[receiver_id],
    )
    reveiver_public_key: Mapped[str] = mapped_column(Text, nullable=True)

    creation_date: Mapped[datetime] = mapped_column(DateTime)
    last_update_date: Mapped[datetime] = mapped_column(DateTime, index=True)

    sent_messages: Mapped[List["SentMessage"]] = db.relationship(back_populates='conversation')
