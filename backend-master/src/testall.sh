#!/bin/bash

folders=("api-gateway" "business" "data-manager")
status=0

export PYTHONPATH=$PWD

for folder in "${folders[@]}"; do
    pushd $folder
    echo "Running test for $folder"
    pytest --cov=main --disable-pytest-warnings \
        --log-file=test.log \
        --log-file-level=DEBUG \
        --log-file-format="%(asctime)s %(levelname)7s %(message)s" \
        --log-file-date-format="%Y-%m-%d %H:%M:%S" \
        test/
    t=$?
    if [ $t -ne 0 ]; then
        status=$t
        echo "Status set to $status"
    fi
    popd
done

echo "Exiting with status $status"
exit $status
