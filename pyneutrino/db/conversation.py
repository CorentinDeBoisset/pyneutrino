from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import Uuid, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ._base import Base

if TYPE_CHECKING:
    from .sent_message import SentMessage
    from .user_account import UserAccount


class Conversation(Base):
    __tablename__ = "conversation"

    id: Mapped[int] = mapped_column(Uuid, primary_key=True)
    creator_id: Mapped[str] = mapped_column(
        Uuid,
        ForeignKey("user_account.id", name="created_conversations_fkey"),
    )
    creator: Mapped["UserAccount"] = relationship(back_populates="created_conversations", foreign_keys=[creator_id])

    invite_code: Mapped[str] = mapped_column(String, nullable=True, unique=True, index=True)

    receiver_id: Mapped[str] = mapped_column(
        Uuid,
        ForeignKey("user_account.id", name="received_conversation_fkey"),
        nullable=True,
    )
    receiver: Mapped["UserAccount"] = relationship(
        back_populates="received_conversations",
        foreign_keys=[receiver_id],
    )

    creation_date: Mapped[datetime] = mapped_column(DateTime)
    last_update_date: Mapped[datetime] = mapped_column(DateTime, index=True)

    sent_messages: Mapped[List["SentMessage"]] = relationship(back_populates="conversation")
