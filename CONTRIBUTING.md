# Contributing

Create a python virtual environment

    $ python -m venv .venv

Activate the virtual environment

    $ (bash) source venv/bin/activate
    $ (powershell) venv\Scripts\Activate.ps1

Install the runtime requirements

    $ pip install -r requirements.txt

Install the development requirements

    $ pip install -r requirements-dev.txt

Check for updates

    $ pip list --outdated

Run linters

    $ black --check .
    $ flake8 --statistics --count --benchmark .

Run tests

    $ pytest --tb=line
    $ coverage run -m pytest

Create database

    $ python manage.py migrate
    $ python manage.py createcachetable
    $ python manage.py createsuperuser
