from flask import Blueprint, jsonify, g, request, session, current_app
from uuid import uuid4
from datetime import datetime
import secrets
from werkzeug.exceptions import BadRequest, NotFound, Conflict, Forbidden
from sqlalchemy import text, select
from sqlalchemy.exc import NoResultFound
from pyneutrino.services import authguard, serialize, validate_schema, login_user
from pyneutrino.db import db, Conversation, UserAccount

ConversationBp = Blueprint("conversation", __name__, url_prefix="/api/messaging/conversations")


@ConversationBp.route("/own")
@authguard
def get_own_conversations():
    try:
        page = int(request.args.get("page", default="1"))
        if page < 1:
            raise ValueError
    except ValueError:
        raise BadRequest("Invalid page value")

    sql = text(
        """
        SELECT c.*
        FROM user_account u
        LEFT JOIN conversation c ON (c.creator_id = u.id OR c.receiver_id = u.id)
        WHERE u.id = :user_id
        ORDER BY c.last_update_date DESC
        LIMIT 10 OFFSET :offset
    """
    )
    params = {"user_id": g.current_user.id, "offset": (page - 1) * 10}
    results = db.session.execute(select(Conversation).from_statement(sql), params).scalars()

    return jsonify(serialize(results, ["id", "creator_id", "receiver_id", "creation_date", "last_update_date"]))


@ConversationBp.route("/new", methods=["POST"])
@authguard
def new_conversation():
    # Only non-guest users can create new conversations
    # FIXME check email validation date instead
    if not g.current_user.email:
        raise Forbidden("Guest users cannot start new conversations")

    new_conversation = Conversation(
        id=uuid4(),
        invite_code=secrets.token_urlsafe(32),
        creator_id=g.current_user.id,
        creation_date=datetime.now(),
        last_update_date=datetime.now(),
    )

    db.session.add(new_conversation)
    db.session.commit()

    return (
        jsonify(serialize(new_conversation, ["id", "creator_id", "receiver_id", "creation_date", "last_update_date"])),
        201,
    )


@ConversationBp.route("/<uuid:id>")
def get_conversation(id: str):
    try:
        conversation: Conversation = db.session.execute(select(Conversation).filter_by(id=id)).scalar_one()
    except NoResultFound:
        raise NotFound

    # There is no authentication guard on this route (since an guest user can use an access code)
    # Therefore, g.current_user is not defined and we read the user_id from session
    if (
        conversation.creator_id == session.get("user_id", "")
        or conversation.receiver_id == session.get("user_id", "")
        or conversation.invite_code == request.args.get("invite_code", default="")
    ):
        # The creator has access to the invite code
        return jsonify(
            serialize(
                conversation, ["id", "invite_code", "creator_id", "receiver_id", "creation_date", "last_update_date"]
            )
        )

    # The user is not allowed to see the conversation.
    # A NotFound is returned to avoid leaking conversation ids.
    raise NotFound


join_schema = {
    "required": ["invite_code"],
    "properties": {
        "invite_code": {"type": "string"},
    },
}


@ConversationBp.route("/<uuid:id>/join", methods=["POST"])
@authguard
@validate_schema(join_schema)
def join_conversation(id: str):
    try:
        conversation: Conversation = db.session.execute(select(Conversation).filter_by(id=id)).scalar_one()
    except NoResultFound:
        raise NotFound

    json_body = request.get_json()

    # If the (uuid/invite code) is invalid, we return a 404 as well
    if conversation.invite_code != json_body["invite_code"]:
        raise NotFound

    if conversation.creator_id == g.current_user.id:
        raise Conflict("The creator of a conversation cannot be on the receiving end")

    if conversation.receiver_id is not None:
        raise Conflict("The conversation already has a receiver")

    conversation.receiver_id = g.current_user.id
    db.session.commit()

    return serialize(conversation, ["id", "creator_id", "receiver_id", "creation_date", "last_update_date"])


guest_join_schema = {
    "required": ["invite_code", "public_key"],
    "properties": {
        "invite_code": {"type": "string"},
        "public_key": {"type": "string"},
    },
}


@ConversationBp.route("/<uuid:id>/guest-join", methods=["POST"])
@validate_schema(guest_join_schema)
def guest_join_conversation(id: str):
    try:
        conversation: Conversation = db.session.execute(select(Conversation).filter_by(id=id)).scalar_one()
    except NoResultFound:
        raise NotFound

    json_body = request.get_json()

    # If the (uuid/invite code) is invalid, we return a 404 as well
    if conversation.invite_code != json_body["invite_code"]:
        raise NotFound

    if "user_id" in session:
        raise Conflict("A logged-in user cannot join a conversation as a guest")

    if conversation.receiver_id is not None:
        raise Conflict("The conversation already has a receiver")

    # Create a new, guest user
    new_user = UserAccount(
        id=uuid4(),
        public_key=json_body["public_key"],
        creation_date=datetime.now(),
    )

    db.session.add(new_user)
    conversation.receiver_id = new_user.id
    db.session.commit()

    login_user(new_user)

    return serialize(new_user, ["id", "creation_date"])
