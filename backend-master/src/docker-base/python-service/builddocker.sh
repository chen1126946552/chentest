#!/bin/bash

env=$1
if [ -z "$env" ]; then
    echo "Missing environment name: ./builddocker <env>"
    exit 1
fi

rm -rf .libs
mkdir .libs
cp -f ../../requirements_shared.txt .libs/
cp -f ../../.pylintrc .libs/
docker build --pull -t reg.ptone.jp/base/uwsgi-nginx-python3.7:$env .
