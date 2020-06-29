#!/bin/bash
encriptar(){
  for var in $(ccdecrypt -c settings.env.cpt); do
    echo "$var"
    # shellcheck disable=SC2163
    export "$var"
  done
}
if [ "$1" == "-c" ]; then
  encriptar
  python3 manage.py check
elif [ "$1" == "-mm" ]; then
  encriptar
  python3 manage.py makemigrations
elif [ "$1" == "-cu" ]; then
  encriptar
  python3 manage.py createsuperuser
elif [ "$1" == "-rs" ]; then
  encriptar
  python3 manage.py runserver 127.0.0.1:9000
elif [ "$1" == "-s" ]; then
  encriptar
  python3 manage.py shell
elif [ "$1" == "-m" ]; then
  encriptar
  python3 manage.py migrate
elif [ "$1" == "-ra" ]; then
  encriptar
  python3 manage.py axes_reset
else
  echo "parametro invalido."
  echo los pametros validos son:
  echo -c para checar
  echo -mm para hacer una migracion
  echo -cu crear un super usuario
  echo -m para migrar
  echo -s para abrir el shell
  echo -rs correr el servicio
  echo -ra resetear acces
fi