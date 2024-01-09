from datetime import datetime
from sqlalchemy import Text, String, Uuid, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from ._base import Base

if TYPE_CHECKING:
    from .conversation import Conversation


class UserAccount(Base):
    __tablename__ = "user_account"

    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    public_key: Mapped[str] = mapped_column(Text)
    private_key: Mapped[str] = mapped_column(Text, nullable=True)
    creation_date: Mapped[datetime] = mapped_column(DateTime)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=True)
    email_verification_code: Mapped[str] = mapped_column(String, nullable=True)
    email_verification_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    created_conversations: Mapped[List["Conversation"]] = relationship(
        back_populates="creator", foreign_keys="Conversation.creator_id"
    )
    received_conversations: Mapped[List["Conversation"]] = relationship(
        back_populates="receiver", foreign_keys="Conversation.receiver_id"
    )

    # We override repr to avoid leaking hashes in logs or errors
    def __repr__(self):
        viewable_dict = {k: v for (k, v) in self.__dict__.items()}
        viewable_dict["password_hash"] = "CENSORED"
        viewable_dict["email_verification_code"] = "CENSORED"

        return f"{self.__class__}({repr(viewable_dict)})"
