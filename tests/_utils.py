from flask import Flask

SQLALCHEMY_DATABASE_URI = "postgresql://pytest:pytestpwd@127.0.0.1:5432/pytest"


def create_basic_user(app: Flask, email="supertest@gmail.com", username="super_username", password="123secret"):
    client = app.test_client()
    client.post(
        "/api/auth/register/new-account",
        json={
            "email": email,
            "username": username,
            "password": password,
            "public_key": f"PGP_PUBLIC_KEY of {username}",
            "private_key": f"PGP_SECRET_KEY of {username}",
        },
    )
