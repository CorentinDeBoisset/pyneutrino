# PyNeutrino

<p align="center">
    <img src="https://github.com/corentindeboisset/pyneutrino/raw/main/frontend-src/src/img/logo_large.svg" alt="Logo of the neutrino application" style="width: 8rem" />
</p>

📮 Send your secrets securely to third-parties, using client-to-client encryption.

This project has many of its features inspired from [Datash](https://github.com/datash/datash) and [PasswordPusher](https://github.com/pglombardo/PasswordPusher).

## ❯ Install

TODO (once a docker package has been made)

## ❯ Contributing

### ❯ Development setup

At first, you should start the database:

```bash
docker compose up -d
```

You can initialize and start the backend with:

```bash
poetry install
poetry run alembic upgrade head
poetry run gunicorn 'pyneutrino:create_app()' --reload
```

If you want to override the configuration of the backend environment, you can follow these steps:

```bash
touch local_config.yaml
# Set values in local_config.yaml
poetry run gunicorn 'pyneutrino:create_app()' --reload --env "NEUTRINO_SETTING_FILE=$(pwd)/local_config.yaml"
```

Once started, you can set up and start the frontend web server:

```bash
cd frontend-src
npm install
npm start
```

The application is then available on http://localhost:4200

Important caveats:
* This project does not use the Flask-SQLAlchemy extension. Do not go to their documentation for insights, but SQLAlchemy's instead.

### Tests

To run the tests, you can execute the following commands:

```
poetry run tox
```

## ❯ Notice

Some content from open-source libraries was used as sources:

* [Twemoji](https://twemoji.twitter.com/) (CC-BY 4.0 Licence)
