# FreeFrom Map Backend

## Overview

Welcome to the FreeFrom Map project backend! This page is under construction so expect more information soon.

## Local Development Setup

This is a Python Flask app. 

#### Set up environment variables

Use the provided template to set up a `.env` file with some environment variables you'll need:

```
cp .env.template .env
```

`.env` is included in the `.gitignore` for this repo and won't be included when you commit your changes.

#### Setup Instructions
This app can be set up either locally or within docker.

[Follow these steps to setup and run it locally](#local-setup)

[Follow these steps to setup and run it in docker](#docker-setup)

### Local Setup
#### Install Python

If you don't already have it installed, install Python 3. You can check that you have it installed using this command:

```
python3 --version
```

This should return something like `Python 3.7.3`.

#### Install Postgres

Install and run a PostgreSQL on your computer.

#### Set up database roles

1. Start a Postgres client session: `psql`
2. Create a new user: `create user "freefrom_map_user";`
3. Create a database: `create database "freefrom_map_dev";`
4. Give the user permissions on your database: `grant all privileges on database freefrom_map_dev to freefrom_map_user;`
5. Quit psql: `\q`

### Set up environment variables

Use the provided template to set up a .env file with some environment variables you'll need:

```
cp .env.template .env
```

`.env` is included in the `.gitignore` for this repo and won't be included when you commit your changes.

While .env.template contains some non-sensitive environment variables, there are a few that you'll
need to get from the team. Ask in the #proj-freefrom-map-dev channel for these variables.

### Start the virtual environment (aka venv)

We use [venv](https://docs.python.org/3/library/venv.html) to ensure that every developer is using the same dependency versions.

```
python3 -m venv env
source env/bin/activate
```

Now, when you run `which python`, you should get something like: `/path/to/your/repo/env/bin/python`. You can deactivate the venv at any time by running `deactivate`.

You only have to run `python3 -m venv env` once, but you should run `source env/bin/activate` every time you work on this repository.

#### Install the requirements

```
pip3 install -r requirements.txt
```

#### Migrate the database

```
python3 manage.py db migrate
python3 manage.py db upgrade
```

If you receive a "Target database is not up to date." error, try `python3 manage.py db stamp head`

#### Running the application

Run the application with the following command:

```
python3 manage.py runserver
```

Then, in your browser, navigate to `localhost:5000/`. You should see the message "Hello world!" on your screen.

### Docker Setup
1. Download latest docker
    1. Make sure `docker --version` returns a version
1. Run `docker-compose up` to build the images.

Then, in your browser, you can navigate to `localhost:5001/categories` and it will return an empty array. 

### Docker Tips
If you need to shell into a container, either the app or db, you can run: `docker exec -it freefrom_map_app /bin/sh`
and you will enter into a shell. This is handy if you prefer `psql` over a Database IDE, or need to hop on the containers
to check something.

## Running tests

Run tests with the following command:

```
python3 -m unittest
```


If in docker, you can run:

```
docker exec -it freefrom_map_app python -m unittest
```

## Linting

Before merging your code, check that it passes the linter (PEP8 style):

```
flake8
```

## API Reference
The following section describes the FreeFrom map backend API. All responses will be formatted as JSON, and all
request bodies should be provided as JSON.

### Categories
A category represents a group of criteria in the map scorecard. A category has the following fields:

|  Name  |   Type  |    Notes    |
|--------|---------|-------------|
| id     | Integer | Primary key |
| title  | String  |             |
| active | Boolean |             |

#### GET /categories

This endpoint returns a list of all existing categories. It will return an empty array if no categories exist.

#### GET /categories/<id>

This endpoint returns one category corresponding to the id provided in the request. If no category with that
id exists, it will return a 404 response code.

### Criteria

A criterion represents one measure in the state scorecard to determine whether a state has strong survivor wealth policies.

|         Name        |   Type   |    Notes    |
|---------------------|----------|-------------|
| id                  | Integer  | Primary key |
| category_id         | Integer  | Foreign key |
| title               | String   |             |
| recommendation_text | String   |             |
| active              | Boolean  |             |

### GET /criteria

This endpoint returns a list of all existing criteria. It will return an empty array if no criteria exist.

### GET /criteria/<id>

This endpoint returns one criterion corresponding to the id provided in the request. If no criterion with that
id exists, it will return a 404 response code.
