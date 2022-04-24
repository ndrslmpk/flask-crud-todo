# Backend

This part of the project consists of the backend.

## Fast-track start

Consists of the essential commands you need to execute to get the project running, while maintaining full control for development. More details follow.

- Start db:
  - `pg_ctl -D "C:/<path_to_PostgreSQL>/PostgreSQL/14/data" start`
- Connect to db:
  - `psql -U <username>`
  - `\connect <database_name>`
- Start flask:
  - `venv/Scripts/activate`
  - `export FLASK_APP=app.py`
  - `flask run`
- Start tailwind cli:
  - `npx tailwindcss -i ./static/src/styles.css -o ./static/css/main.css --watch`

Alternatively, you can run all commands by running the provided script performing `./rundev.sh`

## Tech-Stack

In our setting we are using

- Flask
  - SQLAlchemy
    - PSYCOPG2
  - Jinja2
  - flask_migrate
    - alembic
- PostgreSQL
- Tailwind CSS 3.

## Getting started: Run the app

### Starting the Postgres DB

Check the installation of PostgreSQL.

Start the PostgreSQL database server `pg_ctl -D "C:/<path_to_PostgreSQL>/PostgreSQL/14/data" start`

- `-D` defines the data-directory of the database
- `start` starts the database

**Connect to the PostgreSQL server** using psql
`psql -U <username>` connect to the database using your account. If your default `psql` user is your local machines user name, you might want to change the default psql username to `postgres` by `export PGUSER=postgres` (on Windows).

**Connecting to the database** is performed within the psql cli by executing the connect command followed by the database name. If you are not sure about the name of your database you might want to list all existing databases by `\l`. Now you can connect by typing `\connect <database_name>` or `\c <database_name>`.

### Initializing the flask application

Entrypoint for the application is the `app.py` file

- Start the virtual environment by executing the activate-file in the project environment `venv/Scripts/activate` (it will be displayed by showing `(venv)` in the terminal)
- Set the entry file for the flask project `export FLASK_APP=app.py`
- Start the flask app `flask run`

## Development Process: Setting up the project and understanding tools for development

### Running migrations

If changes to models are performed, those changes shall be managed using migrations to avoid an unexpected loss of data. So if you changed the Model within your flask app (thus changed the PostgreSQL database schema), the following procedure is the common working sequence.

- Let `alembic` (works under the hood of `flask_migrate`) detect changes to your db.Models by executing `flask db migrate`. This will create a migrations file that allows you to adopt a newer version of your database. \_Important: Add a comment by using the `-m` flag to describe the actual changes happened in that particular migration, it will allow the db-changes to be much more understandable. Resulting in the following command to run db migrations:

```
flask db migrate -m "<your descriptive migration message>
```

- Therefore run `flask db upgrade` to let the git-like `flask_migrate` version pointer move to your newer database version. FYI: This command, although it might be pretty obvious is not performed automatically - this created kind of confusion to me in the beginning.
- Not sure which database version you currently using? Use `flask db current` to get the current HEAD of your db.

Find more informations at [alembic-docs](https://alembic.sqlalchemy.org/en/latest/) [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)

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

5. Add a `tailwind.config.js` file and add an initial [content configuration](https://tailwindcss.com/docs/content-configuration) to tell tailwind which HTML templates and JavaScript components should be supported by tailwind. To get more into the details of how to cofigure tailwind properly, watch the docs.

```
module.exports = {
  content: ["./templates/*.{html,js,jsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

6. For the generation of CSS from the tailwind preprocessor directives in `static/src/style.css` into the core css file `static/css/main.css`, we run

```
npx tailwindcss -i ./static/src/styles.css -o ./style/css/main.css
```

- **Remark:** The given flags `-i <input/directory/styling-file.css>` and `-o <output/directory/styling-file.css>` stand for input- and output-directory. From the input directory all applied styling is converted and transfered to the output-directory file. If you furthermore want to make your development process more interactive you might want to automatically update your frontend by inline `html` styling changes. For this purpose you can activate the tailwind cli using

```
npx tailwindcss -i ./static/src/styles.css -o ./style/css/main.css --watch
```

For more details follow the [Installation Guide](https://tailwindcss.com/docs/installation) for Tailwind CLI

Remarks:

- In development mode you want be able to see style changes immediately. ~~So that the [Just-in-Time Mode](https://v2.tailwindcss.com/docs/just-in-time-mode) [Just-in-Time Mode](https://tailwindcss.com/blog/just-in-time-the-next-generation-of-tailwind-css) might be a useful thing.~~

### Modifying migrations

`migrations/alembic.ini` is the configuration file for alembic as the database migration tool for SQLAlchemy.

- modifying the `file_template = <...>` line allows to define a structure for migration files. For instance, we are likely to use a chronical ordering of migration files to clearly be certain of the latest migration file without searching the history of migrations for the latest commit id, which is set as default file name.

### Adding a virtual environment to an existing project

After developing the first functionalities used within the given project, I realized that it is useful to adopt a virtual environment for the project (local) to avoid versioning problems of used tools (e.g., imported libraries) that might collide with the version of your globally installed toolset. A virtual environment can be thought of as a local bubble that allows to separate your project from the rest of your (global) system.
If you ever face that problem you will have to take a snapshot of the currently used tools inside your flask project. Perform a snapshot by executing `pip freeze > requirements.txt` inside the root directory of your project. The output will create a list of tools, which serve the base of (re-)setting up your local virtual environment.

Creating the virtual environment is natively supported when using python 3.x. Check your current python version with `python -V`. If you do use a `python version x.y>3.4`, you might need to find a workaround by using a third-party tool like [virtualenv](https://virtualenv.pypa.io/en/latest/). Performing `python -m venv <venv_name>` creates a new virtual environment directory.

After installing your virtual environment you can start it by activation, using the `. venv/scripts/activate` command (for Windows10). The bash will then display a `venv` inside the terminal, which indicates that you are working inside your virtual environment. . As the initially installed version does not support any external tools or libraries, you are likely required to install the dependencies by `pip install -r requirements.txt`.

Since your installation of python might include hardware specifics, it might lead Keep in mind that the virtual environment should not be part of your git. Instead, add it to your `.gitignore`

### Documentation

Following international conventions on a unified documentation of python code, the [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/) as a Python Enhancement Proposal (PEP) defined conventions to follow.

---

## List of helpful resources adopted while development

- https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask

**Virtual Environment - Requirments - Versioning**

- https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/
- https://stackoverflow.com/questions/55052434/does-python-requirements-file-have-to-specify-version

**Project Structure, API, and web service concepts**

- https://mark.douthwaite.io/getting-production-ready-a-minimal-flask-app/
