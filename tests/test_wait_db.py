from flask import Flask
from pyneutrino import create_app
from ._utils import REDIS_URI


def test_wait_db_command_success(app: Flask):
    runner = app.test_cli_runner()
    result = runner.invoke(args=["wait-db", "--timeout", "1"])
    assert "The database is available" in result.output


def test_wait_db_command_failure():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "postgresql://127.0.0.2:5432/nope?connect_timeout=1",
            "REDIS_URI": REDIS_URI,
        }
    )
    runner = app.test_cli_runner()
    result = runner.invoke(args=["wait-db", "--timeout", "0"])
    assert "Failed to connect to the database" in result.output
