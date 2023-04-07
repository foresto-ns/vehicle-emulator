#!/bin/sh

cd /usr/src/app

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"
