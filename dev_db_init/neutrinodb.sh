#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER neutrino PASSWORD 'neutrinopwd';
	CREATE DATABASE neutrino OWNER neutrino;
EOSQL
