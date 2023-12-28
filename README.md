# PyNeutrino

<p align="center">
    <img src="https://github.com/corentindeboisset/neutrino/raw/main/frontend-src/src/assets/logo_large.svg" alt="Logo of the neutrino application" style="width: 8rem" />
</p>

📮 Send your secrets securely to third-parties, using client-to-client encryption.

This project has many of its features inspired from [Datash](https://github.com/datash/datash) and [PasswordPusher](https://github.com/pglombardo/PasswordPusher).

## ❯ Install

TODO (once a docker package has been made)

## ❯ Contributing

### ❯ Development setup

You can initialize the backend with:

```bash
# TODO: run migrations
poetry run gunicorn 'pyneutrino:create_app()' --reload
```

At the same time, you can set up and start the frontend web server:

```bash
cd frontend-src
npm install
ng serve --open # FIXME: check the commands once angular is setup
```

The application is then available at [http://localhost:8080]

### Tests

To run the tests, you can execute the following commands:

```
poetry run tox
```
