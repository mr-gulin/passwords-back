#!/bin/sh

python manage.py migrate --no-input
uwsgi --ini uwsgi.ini
