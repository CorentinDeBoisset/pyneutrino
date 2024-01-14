from flask import Flask
from ._utils import create_basic_user


def test_new_conversation(app: Flask):
    create_basic_user(app)
    client = app.test_client()
    client.post("/api/auth/session/login", json={"email": "supertest@gmail.com", "password": "123secret"})

    res = client.post("/api/messaging/conversations/new")
    assert res.status_code == 201
    assert res.json["id"] is not None


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
