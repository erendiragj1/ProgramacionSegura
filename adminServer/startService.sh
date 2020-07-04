#!/bin/bash

for var in $(ccdecrypt -c settings.env.cpt); do
    echo "$var"
    # shellcheck disable=SC2163
    export "$var"
done
python3 manage.py check
#python3 manage.py makemigrations
#python3 manage.py migrate
#python3 manage.py createsuperuser
python3 manage.py runserver 0.0.0.0:9000
#python3 manage.py shell
#python3 manage.py axes_reset