from uuid import uuid4
from datetime import datetime
from flask import Blueprint, g, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from pyneutrino.services import authguard, serialize, validate_schema
from pyneutrino.db import db, Conversation, SentMessage


MessagesBp = Blueprint("messages", __name__, url_prefix="/api/messaging/messages")


@MessagesBp.route("")
@authguard
def get_messages_route():
    conversation_id = request.args.get("conversation_id", default=None)
    if conversation_id is None:
        raise BadRequest("A conversation_id is required in query parameters")

    try:
        conversation = db.session.execute(select(Conversation).filter_by(id=conversation_id)).scalar_one()
    except NoResultFound:
        raise NotFound

    # The user is not allowed to see the conversation.
    # A NotFound is returned to avoid leaking conversation ids.
    if conversation.creator_id != g.current_user.id and conversation.receiver_id != g.current_user.id:
        raise NotFound

    # TODO: implement some pagination on the messages
    messages = db.session.execute(conversation.sent_messages.select().limit(10)).scalars()

    return serialize(messages, ["id", "creation_date", "sender", "message"])


new_message_schema = {
    "required": ["message", "conversation_id"],
    "properties": {
        "message": {"type": "string"},
        "conversation_id": {"type": "string"},
    },
}


@MessagesBp.route("/new", methods=["POST"])
@authguard
@validate_schema(new_message_schema)
def new_message_route():
    json_body = request.get_json()

    try:
        conversation = db.session.execute(select(Conversation).filter_by(id=json_body["conversation_id"])).scalar_one()
    except NoResultFound:
        raise NotFound

    new_message = SentMessage(
        id=uuid4(),
        conversation_id=conversation.id,
        sender=g.current_user.id,
        creation_date=datetime.now(),
        message=json_body["message"],
    )
    db.session.add(new_message)
    db.session.commit()

    # TODO: send a notification to connected users

    return jsonify(serialize(new_message, ["id", "creation_date", "sender", "message"]))
