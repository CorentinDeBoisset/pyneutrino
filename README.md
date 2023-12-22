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

TODO: make a simple production setup

Start the database using docker compose with:

    docker compose up -d

By default, the connection url to the database is: `neutrino:neutrinopwd@localhost:3306/neutrino`

<!-- TODO: add a start of the backend loop -->

Finally, you can set up and start the frontend web server:

```bash
cd frontend-src
npm install
npm run serve # FIXME
```

The application is then available at [http://localhost:8080]
