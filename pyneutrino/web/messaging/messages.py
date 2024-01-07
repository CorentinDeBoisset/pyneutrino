from flask import Blueprint, g, request
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy.exc import NoResultFound
from pyneutrino.services import authguard, serialize
from pyneutrino.db import db, Conversation


MessagesBp = Blueprint('messages', __name__, url_prefix="/api/messaging/messages")


@MessagesBp.route("")
@authguard
def get_messages():
    conversation_id = request.params.get("conversation_id")
    if conversation_id is None:
        raise BadRequest("A conversation_id is required in query parameters")

    try:
        conversation: Conversation = db.session.execute(
            db.session.query(Conversation).filter_by(id=conversation_id)
        ).scalar_one()
    except NoResultFound:
        raise NotFound

    # The user is not allowed to see the conversation.
    # A NotFound is returned to avoid leaking conversation ids.
    if conversation.creator_id != g.current_user.id and conversation.receiver_id != g.current_user.id:
        raise NotFound

    return serialize(conversation.sent_messages, ["id"])
