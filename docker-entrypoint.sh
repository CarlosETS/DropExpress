#!/bin/bash

cd /app

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py initadmin
exec "$@"