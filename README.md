# Backend

This part of the project consists of the backend.

## Tech-Stack

In our setting we are using

- Flask
- SQLAlchemy
  - PSYCOPG2
  - Jinja2
  - flask_migrate
  - alembic
- PostgreSQL

## Starting the Postgres DB

Check the installation of PostgreSQL.

Start the PostgreSQL database `pg_ctl -D "C:/<path_to_PostgreSQL>/PostgreSQL/14/data" start`

- `-D` defines the data-directory of the database
- `start`starts the database

Connect to the database using psql
`psql -U <username>` connect to the database using your account. If your default `psql` user is your local machines user name, you might want to change the default psql username to `postgres` by `export PGUSER=postgres` (on Windows).

## Initializing the flask application

Entrypoint for the application is the `app.py` file

- Start the virtual environment by executing the activate-file in the project environment `venv/Scripts/activate` (it will be displayed by showing `(venv)` in the terminal)
- Set the entry file for the flask project `export FLASK_APP=app.py`
- Start the flask app `flask run`

## Running migrations

If changes to models are performed, those changes shall be managed using migrations to avoid an unexpected loss of data. So if you changed the Model within your flask app (thus changed the PostgreSQL database schema), the following procedure is the common working sequence.

- Let `alembic` (works under the hood of `flask_migrate`) detect changes to your db.Models by executing `flask db migrate`. This will create an migrationsfile that allows you to adopt a newer version of your database.
- Therefore run `flask db upgrade` to let the git-like `flask_migrate` version pointer move to your newer database version. FYI: This command, although it might be pretty obvious is not performed automatically - this created kind of confusion to me in the beginning.

Find more informations at [alembic-docs]{https://alembic.sqlalchemy.org/en/latest/} [flask-migrate]{https://flask-migrate.readthedocs.io/en/latest/}
