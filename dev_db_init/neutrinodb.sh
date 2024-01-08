#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER neutrino PASSWORD 'neutrinopwd';
	CREATE DATABASE neutrino OWNER neutrino;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER neutrinotest PASSWORD 'neutrinotestpwd';
	CREATE DATABASE neutrinotest OWNER neutrinotest;
EOSQL
