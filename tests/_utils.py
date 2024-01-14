from flask import Flask


def create_basic_user(app: Flask):
    client = app.test_client()
    client.post(
        "/api/auth/register/new-account",
        json={
            "email": "supertest@gmail.com",
            "username": "super_username",
            "password": "123secret",
            "public_key": "PGP_PUBLIC_KEY",
            "private_key": "PGP_SECRET_KEY",
        },
    )
