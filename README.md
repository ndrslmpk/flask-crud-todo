# Backend

This part of the project consists of the backend.

## Tech-Stack

In our setting we are using

Flask
-- SQLAlchemy
--- PSYCOPG2
-- Jinja2
PostgreSQL

## Starting the Postgres DB

Check the installation of PostgreSQL.

Start the PostgreSQL database `pg_ctl -D "C:/<path_to_PostgreSQL>/PostgreSQL/14/data" start`
-- `-D` defines the data-directory of the database
-- `start`starts the database

Connect to the database using psql
`psql -U <username>` connect to the database using your account. If your default `psql` user is your local machines user name, you might want to change the default psql username to `postgres` by `export PGUSER=postgres` (on Windows).

## Initializing the flask application

Entrypoint for the application is the `app.py` file

-- Start the virtual environment by executing the activate-file in the project environment `venv/Scripts/activate` (it will be displayed by showing `(venv)` in the terminal)
-- Set the entry file for the flask project `export FLASK_APP=app.py`
-- Start the flask app `flask run`
