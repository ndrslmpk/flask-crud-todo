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
- Not sure which database version you currently using? Use `flask db current` to get the current HEAD of your db.

Find more informations at [alembic-docs]{https://alembic.sqlalchemy.org/en/latest/} [flask-migrate]{https://flask-migrate.readthedocs.io/en/latest/}

## Setting up the project

### Setting up tailwind

1. Creating a `/static´ folder for all of our assets, css files and js scripts.
2. In the following `yarn` is being used to initialize the project by running the `yarn init`. You might want to use `npm` which will work the same. It will set up a `node_modules` directory which will include the relevant dependencies needed to use tailwind. As a beginner you might want to associate it with something like a hidden library, which includes all the lower level components to let your module run.
3. Install tailwing by running `yarn add tailwindcss`.
4. Add a `src` directory and a `style.css` file. Here you add

```
@tailwind base;
@tailwind components;
@tailwind utilities;
```

5. For the generation of CSS from the tailwind preprocessor directives in `static/src/style.css` into the core css file `static/css/main.css`, we run `npx tailwindcss -i ./src/style.css -o css/main.css`
6. Add a `tailwdind.config.css` file and add an initial [content configuration](https://tailwindcss.com/docs/content-configuration) to tell tailwind which HTML templates and JavaScript components should be supported by tailwind. To get more into the details of how to cofigure tailwind properly, watch the docs.

```
module.exports = {
  content: [
    './templates/**/*.{html,js}',
  ],
  // ...
}
```
