# SQLModel Tutor

## Init command
`pyenv local 3.12.2`
`python -m venv .venv` create venv
`. .venv/bin/activate` enter virtual env
`poetry init`
`poetry add fastapi sqlmodel asyncpg`

## Create PostgreSQL table in local without docker
```shell
psql postgres
# or
# sudo -u postgres psql postgres

# If you didn't create user
# postgres=# CREATE USER postgres WITH PASSWORD 'postgres';

postgres=# CREATE DATABASE sqlmodel_tutor;
postgres=# GRANT ALL PRIVILEGES ON DATABASE "sqlmodel_tutor" to postgres;
```

## Command
`python main.py init-db` initial db schema
`fastapi dev main.py` run fastapi development environment