#!/bin/bash

for var in $(ccdecrypt -c settings.env.cpt); do
    echo "$var"
    export "$var"
done
python manage.py check
python manage.py runserver 127.0.0.1:8000