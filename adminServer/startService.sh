#!/bin/bash

for var in $(ccdecrypt -c settings.env.cpt); do
    echo "$var"
    # shellcheck disable=SC2163
    export "$var"
done
python3 manage.py check
python3 manage.py runserver
#agregar shell, migraciones, runserver
