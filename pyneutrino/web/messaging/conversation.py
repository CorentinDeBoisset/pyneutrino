from flask import Blueprint, jsonify, g, request
from uuid import uuid4
from datetime import datetime
import secrets
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound
from pyneutrino.services import authguard, serialize
from pyneutrino.db import db, Conversation

ConversationBp = Blueprint('conversation', __name__, url_prefix="/api/messaging/conversations")


@ConversationBp.route("/own")
@authguard
def get_own_conversations():
    try:
        page = int(request.args.get("page", default="1"))
        if page < 1:
            raise ValueError
    except ValueError:
        raise BadRequest("Invalid page value")

    sql = text("""
        SELECT c.*
        FROM user_account u
        LEFT JOIN conversation c ON (c.creator_id = u.id OR c.receiver_id = u.id)
        WHERE u.id = :user_id
        ORDER BY c.last_update_date DESC
        LIMIT 10 OFFSET :offset
    """)
    params = {
        "user_id": g.current_user.id,
        "offset": (page-1)*10
    }
    results = db.session.execute(db.session.query(Conversation).from_statement(sql), params).scalars()

    return jsonify(serialize(
        results,
        ["id", "creator_id", "receiver_id", "creation_date", "last_update_date"]
    ))


@ConversationBp.route("/new", methods=["POST"])
@authguard
def new_conversation():
    new_conversation = Conversation(
        id=uuid4(),
        invite_code=secrets.token_urlsafe(32),
        creator_id=g.current_user.id,
        creation_date=datetime.now(),
        last_update_date=datetime.now(),
    )

    db.session.add(new_conversation)
    db.session.commit()

    return jsonify(serialize(
        new_conversation,
        ["id", "creator_id", "receiver_id", "creation_date", "last_update_date"]
    )), 201


@ConversationBp.route("/<uuid:id>")
@authguard
def get_conversation(id: str):
    try:
        conversation: Conversation = db.session.execute(db.session.query(Conversation).filter_by(id=id)).scalar_one()
    except NoResultFound:
        raise NotFound

    if conversation.creator_id == g.current_user.id:
        # The creator has access to the invite code
        return jsonify(serialize(
            conversation,
            ["id", "invite_code", "creator_id", "receiver_id", "creation_date", "last_update_date"]
        ))

    if conversation.receiver_id == g.current_user.id:
        return jsonify(serialize(
            conversation,
            ["id", "creator_id", "receiver_id", "creation_date", "last_update_date"]
        ))

    # The user is not allowed to see the conversation.
    # A NotFound is returned to avoid leaking conversation ids.
    raise NotFound


@ConversationBp.route("/<uuid:id>/join")
@authguard
def join_conversation(id: str):
    try:
        conversation: Conversation = db.session.execute(db.session.query(Conversation).filter_by(id=id)).scalar_one()
    except NoResultFound:
        raise NotFound

    # If the (uuid/invite code) is invalid, we return a 404 as well
    if conversation.invite_code == request.args.get('invite_code', default=None):
        raise NotFound

    if conversation.creator_id == g.current_user.id:
        raise Conflict("The creator of a conversation cannot be on the receiving end")

    if conversation.receiver_id is not None:
        raise Conflict("The conversation already has a receiver")

    conversation.receiver_id = g.current_user.id
    db.session.commit()

    return jsonify(serialize(
        conversation,
        ["id", "creator_id", "receiver_id", "creation_date", "last_update_date"]
    ))
