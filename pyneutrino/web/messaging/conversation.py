from flask import Blueprint, jsonify, g, request
from uuid import uuid4
from datetime import datetime
from werkzeug.exceptions import BadRequest
from sqlalchemy import text
from pyneutrino.services import authguard, serialize
from pyneutrino.db import db, Conversation

ConversationBp = Blueprint('conversation', __name__, url_prefix="/api/messaging/conversation")


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
        WHERE u.id = :uid
        ORDER BY c.last_update_date DESC
        LIMIT 10 OFFSET :offset
    """)
    params = {
        "uid": g.current_user.id,
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
