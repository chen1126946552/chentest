#!/bin/bash

service=$1
if [ -z "$service" ]; then
    echo "Missing service name: ./builddocker <service>"
    exit 1
fi

rm -rf .libs
find ./common/ -name '*.py' | cpio -pdm ./$service/.libs/common
cp -f requirements_shared.txt ./$service/.libs/
cp -f .pylintrc ./$service/.libs/

docker build --pull -f $service/Dockerfile -t $service ./$service
