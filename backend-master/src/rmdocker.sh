#!/bin/bash

service=$1
if [ -z "$service" ]; then
    echo "Missing service name"
    exit 1
fi
docker stop $service
docker rm $service
