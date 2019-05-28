#!/bin/bash

status=0
export PYTHONPATH="$(pwd)"
for dir in ./* ; do
  if [ -d "$dir" ]; then

    echo "Linting $dir"

    if [ "$dir" = "./common" ]; then
        # common folder is a package by itself, so run pylint directly on it
        pylint --rcfile .pylintrc $dir
        t=$?
    else
        pushd $dir
        # find all .py files in service folder and run lint
        if [ -n "$(find . -iname "*.py" | grep -iv "migrations" | grep -iv "test")" ]; then
            find . -iname "*.py" | grep -iv "migrations" | grep -iv "test" | xargs pylint --rcfile ../.pylintrc
            t=$?
            else t=0
        fi
        popd
    fi

    if [ $t -ne 0 ]; then
        status=$t
        echo "Status set to $status"
    fi    
  fi
done

echo "Exiting with status $status"
exit $status
