import pytest
from pyneutrino import create_app
from sqlalchemy import create_engine, text

SQLALCHEMY_DATABASE_URL = "postgresql://pytest:pytestpwd@127.0.0.1:5432/pytest"


@pytest.fixture
def alembic_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    yield engine

    # When executing the tear down,
    # clean up the database by destroying the default schema
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.commit()


@pytest.fixture()
def app(alembic_runner):
    # Execute the migrations before instanciating the app
    alembic_runner.migrate_up_to("heads", return_current=False)

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": SQLALCHEMY_DATABASE_URL,
            "DISABLE_CSRF": True,
        }
    )

    yield app
