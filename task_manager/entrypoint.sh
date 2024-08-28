#!/bin/sh

python manage.py makemigrations
python manage.py migrate
pytest
python manage.py runserver 0.0.0.0:8000

exec "$@"
