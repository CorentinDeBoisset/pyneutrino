import re
from pyneutrino import create_app
from ._utils import create_basic_user, SQLALCHEMY_DATABASE_URI


def test_valid_xsrf(alembic_runner):
    # Execute the migrations before instanciating the app
    alembic_runner.migrate_up_to("heads", return_current=False)
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": SQLALCHEMY_DATABASE_URI,
        }
    )
    create_basic_user(app)

    client = app.test_client()

    res = client.post("/api/auth/session/login", json={"email": "supertest@gmail.com", "password": "123secret"})
    headers = " ".join(res.headers.getlist("Set-Cookie"))
    assert "XSRF-TOKEN=" in headers
    token = re.search("XSRF-TOKEN=(.*?);", headers)

    # Check the requests suceeds when we set the XSRF token
    res = client.post("/api/auth/session/logout", headers={"X-XSRF-TOKEN": token.group(1)})
    assert res.status_code == 204


def test_absent_xsrf(alembic_runner):
    # Execute the migrations before instanciating the app
    alembic_runner.migrate_up_to("heads", return_current=False)
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": SQLALCHEMY_DATABASE_URI,
        }
    )
    create_basic_user(app)

    client = app.test_client()

    res = client.post("/api/auth/session/login", json={"email": "supertest@gmail.com", "password": "123secret"})

    # Test a post request without the token
    res = client.post("/api/auth/session/logout")
    assert res.status_code == 401
    assert res.json["description"] == "A XSRF token must be sent in the X-XSRF-TOKEN header"


def test_invalid_xsrf(alembic_runner):
    # Execute the migrations before instanciating the app
    alembic_runner.migrate_up_to("heads", return_current=False)
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": SQLALCHEMY_DATABASE_URI,
        }
    )
    create_basic_user(app)

    client = app.test_client()

    res = client.post("/api/auth/session/login", json={"email": "supertest@gmail.com", "password": "123secret"})

    # Test a post request without the token
    res = client.post("/api/auth/session/logout", headers={"X-XSRF-TOKEN": "invalid-value"})
    assert res.status_code == 401
    assert res.json["description"] == "Invalid XSRF Token"
