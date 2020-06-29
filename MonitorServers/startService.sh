#!/bin/bash

for var in $(ccdecrypt -c settings.env.cpt); do
    echo "$var"
    export "$var"
done
python3 manage.py check
#python3 manage.py makemigrations
#python3 manage.py migrate
#python3 manage.py createsuperuser
python3 manage.py runserver 127.0.0.1:8000
#python3 manage.py shell