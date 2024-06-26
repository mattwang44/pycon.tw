### Requirements
- Docker Engine 1.13.1+
- Docker Compose 1.10.0+

# Containerized Development Environment

1. Edit the `DATABASE_URL` in `src/pycontw2016/settings/local.env`(Copy from [`local.sample.env`](../src/pycontw2016/settings/local.sample.env)). Use the Postgres username, password, database name, and port configured in [`./docker-compose-dev.yml`](../docker-compose-dev.yml).

    ```
    DATABASE_URL=postgres://postgres:secretpostgres@db:5432/pycontw2016
    ```

2. Simply run the following command to install all dependencies, activate a containerized Postgres server, and enter into a poetry shell inside the application container (<code>ctrl+c</code> to quit).

    ```
    ./enter_dev_env.sh
    ```

3. In the shell, you can run any commands as if you are in a local development environment. Here are some common Django commands:

    ```sh
    # make migrations
    python manage.py makemigrations

    # apply migrations
    python manage.py migrate

    # create a superuser
    python manage.py createsuperuser

    # pull out strings for translations
    python manage.py makemessages -l en_US -l zh_Hant

    # compile translations
    python manage.py compilemessages

    # run the dev server (you can access the site at http://localhost:8000/)
    python manage.py runserver 0.0.0.0:8000
    ```
