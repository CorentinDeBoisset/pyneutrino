from flask import Flask


def test_registration(app: Flask):
    client = app.test_client()
    res = client.post(
        "/api/auth/register/new-account",
        json={
            "email": "supertest@gmail.com",
            "username": "myspername",
            "password": "123secret",
            "public_key": "PGP_PUBLIC_KEY",
            "private_key": "PGP_SECRET_KEY",
        },
    )

    assert res.status_code == 201
