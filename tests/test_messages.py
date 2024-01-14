from flask import Flask
from ._utils import create_basic_user


def test_send_message(app: Flask):
    # Setup the users, and start a conversation
    create_basic_user(app, email="creator@neutri.no", username="creator_username")
    create_basic_user(app, email="receiver@neutri.no", username="receiver_username")
    create_basic_user(app, email="snooper@neutri.no", username="snooper_username")

    creator_client = app.test_client()
    creator_client.post("/api/auth/session/login", json={"email": "creator@neutri.no", "password": "123secret"})

    receiver_client = app.test_client()
    receiver_client.post("/api/auth/session/login", json={"email": "receiver@neutri.no", "password": "123secret"})

    snooper_client = app.test_client()
    snooper_client.post("/api/auth/session/login", json={"email": "snooper@neutri.no", "password": "123secret"})

    res = creator_client.post("/api/messaging/conversations/new")
    conv_id = res.json["id"]
    res = creator_client.get(f"/api/messaging/conversations/{conv_id}")
    invite_code = res.json["invite_code"]

    res = receiver_client.post(
        f"/api/messaging/conversations/{conv_id}/join",
        json={"invite_code": invite_code},
    )

    # Get the message list
    res = creator_client.get(f"/api/messaging/messages?conversation_id={conv_id}")
    assert res.status_code == 200
    assert len(res.json) == 0

    # Create a new message
    res = creator_client.post(
        "/api/messaging/messages/new", json={"message": "ENCRYPTED-MESSAGE", "conversation_id": conv_id}
    )
    assert res.status_code == 200
    assert res.json["message"] == "ENCRYPTED-MESSAGE"

    # Check another user can neither access the messages, nor send one
    res = snooper_client.get(f"/api/messaging/messages?conversation_id={conv_id}")
    assert res.status_code == 404
    res = snooper_client.post(
        "/api/messaging/messages/new", json={"message": "FAKE-MESSAGE", "conversation_id": conv_id}
    )
    assert res.status_code == 404
