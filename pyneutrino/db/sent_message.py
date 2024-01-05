from datetime import datetime
from sqlalchemy import DateTime, Text, Uuid, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING
from ._db import db

if TYPE_CHECKING:
    from .conversation import Conversation


# known bug: https://github.com/python/mypy/issues/8603
class SentMessage(db.Model):  # type: ignore[name-defined]
    id: Mapped[int] = mapped_column(Uuid, primary_key=True)
    conversation_id: Mapped[str] = mapped_column(Uuid, ForeignKey("conversation.id", name="conversation_fkey"))
    conversation: Mapped["Conversation"] = db.relationship(
        back_populates='sent_messages',
        foreign_keys=[conversation_id]
    )
    sender: Mapped[str] = mapped_column(Uuid, ForeignKey("user_account.id", name="sender_fkey"))
    creation_date: Mapped[datetime] = mapped_column(DateTime)
    message: Mapped[int] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index('ix_conversation_message_order', 'conversation_id', 'creation_date'),
    )
