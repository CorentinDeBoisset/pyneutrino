import sys
import time
import click
from flask import Blueprint
from sqlalchemy import text
from pyneutrino.db import db
from sqlalchemy.exc import OperationalError

WaitDbBp = Blueprint("wait_db", __name__, cli_group=None)


@WaitDbBp.cli.command("wait-db")
@click.option("-t", "--timeout", type=int, default=30)
def wait_db_command(timeout: int):
    start = time.time()
    while True:
        try:
            db.session.execute(text("SELECT 1"))
            print("The database is available")
            sys.exit(0)
        except OperationalError:
            pass
        finally:
            db.session.close()

        if time.time() > start + timeout:
            print(f"Failed to connect to the database after {time.time() - start}s")
            sys.exit(1)

        time.sleep(5)
