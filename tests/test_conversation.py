from flask import Flask
from ._utils import create_basic_user


def test_new_conversation(app: Flask):
    create_basic_user(app)
    client = app.test_client()
    client.post("/api/auth/session/login", json={"email": "supertest@gmail.com", "password": "123secret"})

    res = client.post("/api/messaging/conversations/new")
    assert res.status_code == 201
    assert res.json["id"] is not None

    unlogged_client = app.test_client()
    res = unlogged_client.post("/api/messaging/conversations/new")
    assert res.status_code == 401


def test_get_conversations(app: Flask):
    create_basic_user(app)
    client = app.test_client()
    client.post("/api/auth/session/login", json={"email": "supertest@gmail.com", "password": "123secret"})

    res = client.get("/api/messaging/conversations/own")
    assert res.status_code == 200
    assert len(res.json) == 0

    client.post("/api/messaging/conversations/new")

    res = client.get("/api/messaging/conversations/own")
    assert res.status_code == 200
    assert len(res.json) == 1
    conv_id = res.json[0]["id"]

    res = client.get(f"/api/messaging/conversations/{conv_id}")
    assert res.status_code == 200
    assert res.json["id"] == conv_id


def test_guest_join_conversation(app: Flask):
    create_basic_user(app)
    creator_client = app.test_client()
    creator_client.post("/api/auth/session/login", json={"email": "supertest@gmail.com", "password": "123secret"})
    res = creator_client.post("/api/messaging/conversations/new")
    conv_id = res.json["id"]

    res = creator_client.get(f"/api/messaging/conversations/{conv_id}")
    invite_code = res.json["invite_code"]

    guest_client = app.test_client()

    # Test an invalid invite code
    res = guest_client.post(
        f"/api/messaging/conversations/{conv_id}/guest-join",
        json={"invite_code": "invalid-invite-code", "public_key": "guest-pubkey"},
    )
    assert res.status_code == 404

    # Check we can join the conversation with a guest account
    res = guest_client.post(
        f"/api/messaging/conversations/{conv_id}/guest-join",
        json={"invite_code": invite_code, "public_key": "guest-pubkey"},
    )
    assert res.status_code == 200
    guest_id = res.json["id"]

    res = creator_client.get(f"/api/messaging/conversations/{conv_id}")
    assert res.json["receiver_id"] == guest_id

    # Check we cannot join a second time
    unlogged_client = app.test_client()
    res = unlogged_client.post(
        f"/api/messaging/conversations/{conv_id}/guest-join",
        json={"invite_code": invite_code, "public_key": "guest-pubkey"},
    )
    assert res.status_code == 409


def test_join_conversation(app: Flask):
    create_basic_user(app, email="creator@neutri.no", username="creator_username")
    create_basic_user(app, email="receiver@neutri.no", username="receiver_username")
    create_basic_user(app, email="snooper@neutri.no", username="snooper_username")

    creator_client = app.test_client()
    res = creator_client.post("/api/auth/session/login", json={"email": "creator@neutri.no", "password": "123secret"})
    creator_id = res.json["id"]

    res = creator_client.post("/api/messaging/conversations/new")
    conv_id = res.json["id"]

    res = creator_client.get(f"/api/messaging/conversations/{conv_id}")
    invite_code = res.json["invite_code"]

    receiver_client = app.test_client()
    res = receiver_client.post("/api/auth/session/login", json={"email": "receiver@neutri.no", "password": "123secret"})
    receiver_id = res.json["id"]

    # Test an invalid invite code
    res = receiver_client.post(
        f"/api/messaging/conversations/{conv_id}/join",
        json={"invite_code": "invalid-invite-code"},
    )
    assert res.status_code == 404

    # Check we can join the conversation with an existing account
    res = receiver_client.post(
        f"/api/messaging/conversations/{conv_id}/join",
        json={"invite_code": invite_code},
    )
    assert res.status_code == 200
    assert res.json["id"] == conv_id

    res = creator_client.get(f"/api/messaging/conversations/{conv_id}")
    assert res.json["receiver_id"] == receiver_id
    assert res.json["creator_id"] == creator_id

    # Check we cannot join a second time
    res = receiver_client.post(
        f"/api/messaging/conversations/{conv_id}/join",
        json={"invite_code": invite_code},
    )
    assert res.status_code == 409

    res = receiver_client.get(f"/api/messaging/conversations/{conv_id}/public_keys")
    assert res.status_code == 200
    assert res.json["creator_public_key"] == "PGP_PUBLIC_KEY of creator_username"
    assert res.json["receiver_public_key"] == "PGP_PUBLIC_KEY of receiver_username"

    # Check another user cannot access anything
    snooper_client = app.test_client()
    snooper_client.post("/api/auth/session/login", json={"email": "snooper@neutri.no", "password": "123secret"})

    res = snooper_client.get(f"/api/messaging/conversations/{conv_id}")
    assert res.status_code == 404
    res = snooper_client.get(f"/api/messaging/conversations/{conv_id}/public_keys")
    assert res.status_code == 404
