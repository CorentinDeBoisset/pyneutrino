##
# Step to build the frontend assets
##
FROM node:20-alpine as frontend-builder

RUN mkdir /neutrino

# Install the dependencies only
# (before the code is added to improve image caching)
COPY frontend-src/package.json frontend-src/package-lock.json /neutrino
RUN cd /neutrino && \
    npm ci --audit=false --fund=false

# Build the frontend assets
COPY frontend-src /neutrino
RUN cd /neutrino && \
    npm run build


##
# Step to build the backend assets
##
FROM python:3.12-alpine as backend-builder

# Setup poetry
RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry config virtualenvs.options.no-pip true && \
    poetry config virtualenvs.options.no-setuptools true

# Create the directories
RUN mkdir neutrino && \
    mkdir /neutrino/pyneutrino /neutrino/migrations && \
    mkdir /neutrino/pyneutrino/templates /neutrino/pyneutrino/static

COPY pyproject.toml poetry.lock /neutrino

# Install the dependencies only
# (before the code is added to improve image caching)
RUN cd /neutrino && \
    poetry install --only main --no-root

# Copy the code
COPY alembic.ini /neutrino
COPY pyneutrino /neutrino/pyneutrino
COPY migrations /neutrino/migrations

# Install and pre-build the python package
RUN cd /neutrino && \
    poetry install --only main --compile


##
# Final image
##
FROM python:3.12-alpine

# TODO: add a user

RUN mkdir /neutrino

# Backend assets, easy-peasy
COPY --from=backend-builder /neutrino /neutrino

# Frontend assets, making a special case for the home.html template
COPY --from=frontend-builder /neutrino/dist/browser/home.html /neutrino/pyneutrino/templates/
COPY --from=frontend-builder /neutrino/dist/browser/* /neutrino/pyneutrino/static

# Copy entrypoint and configuration
COPY --chmod=0755 docker_build/entrypoint.sh /entrypoint.sh
COPY docker_build/gunicorn.conf.py /etc/gunicorn.conf.py

WORKDIR /neutrino
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/neutrino/.venv/bin/python", "-m", "gunicorn", "--config=/etc/gunicorn.conf.py"]
