# Social Network API
this is a simple REST API-based social network in Django where
Users can sign up and create text posts and view, like, and unlike other Users’ posts.

## Used Technical Tools
* `Django` for the project.
* `Django-rest-framework` library for API.
* `JWT` for user authentication.
* `Celery` for tasks.
* `Abstractapi` for email validation, geolocation and holiday purposes.

## General Requirements
* [Redis](https://redis.io/docs/getting-started/installation/)
* [Python3](https://www.python.org/downloads/)

## Setup (macOS & Linux)

To try the project, set up a virtual environment and install the listed dependencies:

```sh
$ python3 -m pip install virtualenv
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ python3 -m pip install -r requirements.txt
```

## Setup (Windows)

To try the project, set up a virtual environment and install the listed dependencies:

```sh
$ py -m pip install --user virtualenv
$ py -m venv venv
$ .\venv\Scripts\activate
(venv) $ py -m pip install -r requirements.txt
```
Once you've installed all the dependencies, you need to start three processes that need to run at the same time:

1. API
2. Redis
3. Celery

To get all of them running, open three different terminal windows and start them one-by-one:

**API:**

```sh
(venv) $ python manage.py runserver
```

**Redis server:**

```sh
$ redis-server
```

**Celery:**

```sh
(venv) $ python -m celery -A social worker -l info
```
## Project Docs
* The API endpoints should be now running under `http://127.0.0.1:8000/swagger` (if port 8000 is available)

## Authentication
* Create account from: `http://127.0.0.1:8000/user/register/`.
* Go to `http://127.0.0.1:8000/user/login/` to get user token.
* Then go to swagger authorize part and type: `Bearer <YOUR_ACCESS_TOKEN>`, now you are logged in.

## Run Tests
* To Run unit tests : `python3 manage.py test`.


## Admin Dashboard
* To access Admin dashboard : `http://127.0.0.1:8000/admin` and the admin credentials are: `admin@admin.admin`, `admin@1234`