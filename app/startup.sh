#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py compilemessages --no-input
gunicorn --bind=0.0.0.0 --timeout 600 --chdir app config.wsgi
