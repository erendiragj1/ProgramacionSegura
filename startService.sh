#!/bin/bash

for var in $(ccdecrypt -c settings.env.cpt); do
    #echo "$var"
    export "$var"
done

docker-compose build 
docker-compose --compatibility up -d