#!/bin/sh

set -o pipefail

if [ "$1" = "/neutrino/.venv/bin/python" ] && [ "$2" = "-m" ] && [ "$3" = "gunicorn" ]; then
    # If the main command is to start gunicorn, we automatically run the migrations
    /neutrino/.venv/bin/python -m flask --app pyneutrino test wait-db --timeout 10
    [ $? -eq 0 ] && /neutrino/.venv/bin/python -m alembic upgrade heads
fi

exec "$@"
