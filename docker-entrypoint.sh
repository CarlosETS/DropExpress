#!/bin/bash

cd /app


python manage.py makemigrations
python manage.py migrate
python manage.py initadmin
python manage.py initproduct
exec "$@"