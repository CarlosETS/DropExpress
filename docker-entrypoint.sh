#!/bin/bash

cd /app

python manage.py makemigrations user
python manage.py makemigrations product
python manage.py makemigrations cart
python manage.py migrate
python manage.py initadmin
python manage.py initproduct
exec "$@"