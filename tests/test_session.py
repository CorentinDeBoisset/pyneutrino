from flask import Flask
from ._utils import create_basic_user


def test_valid_login(app: Flask):
    create_basic_user(app)
    client = app.test_client()
    res = client.post("/api/auth/session/login", json={"email": "supertest@gmail.com", "password": "123secret"})
    assert res.json["id"] is not None

    headers = " ".join(res.headers.getlist("Set-Cookie"))

    # Check that a session coookie is created
    assert "session=" in headers


def test_invalid_login(app: Flask):
    create_basic_user(app)
    client = app.test_client()
    res = client.post("/api/auth/session/login", json={"email": "supertest@gmail.com", "password": "wrong"})
    assert res.status_code == 401


def test_logout(app: Flask):
    create_basic_user(app)
    client = app.test_client()

    # Check we cannot logout without being authenticated
    res = client.post("/api/auth/session/logout")
    assert res.status_code == 401

    # Login and Logout
    client.post("/api/auth/session/login", json={"email": "supertest@gmail.com", "password": "123secret"})
    res = client.post("/api/auth/session/logout")
    assert res.status_code == 204
    print(" ".join(res.headers.getlist("Set-Cookie")))
    assert "session=;" in " ".join(res.headers.getlist("Set-Cookie"))
