#!/bin/bash

service=$1
port=$2

if [ -z "$service" ]; then
    echo "Missing service name: ./rundocker <service> [<port>]"
    exit 1
fi

case "$service" in
    "api-gateway")
        service_port=9080;;
    "business")
        service_port=9081;;
    "data-manager")
        service_port=9082;;
    *) 
        echo "Unknown service $service"
        exit 1;;
esac

if [ -z "$port" ]; then
    port=$service_port
fi

echo "Building docker for service $service"
./builddocker.sh $service

echo "Starting service on port $port"

./rmdocker.sh $service >/dev/null 2>&1
docker run -p $port:$service_port -d --name $service $service
