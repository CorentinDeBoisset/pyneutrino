from datetime import datetime
from sqlalchemy import DateTime, Text, Uuid, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from ._base import Base

if TYPE_CHECKING:
    from .conversation import Conversation


class SentMessage(Base):
    __tablename__ = "sent_message"

    id: Mapped[int] = mapped_column(Uuid, primary_key=True)
    conversation_id: Mapped[str] = mapped_column(Uuid, ForeignKey("conversation.id", name="conversation_fkey"))
    conversation: Mapped["Conversation"] = relationship(back_populates="sent_messages", foreign_keys=[conversation_id])
    sender: Mapped[str] = mapped_column(Uuid, ForeignKey("user_account.id", name="sender_fkey"))
    creation_date: Mapped[datetime] = mapped_column(DateTime)
    message: Mapped[int] = mapped_column(Text, nullable=True)

    __table_args__ = (Index("ix_conversation_message_order", "conversation_id", "creation_date"),)
