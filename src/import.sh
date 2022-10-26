#!/bin/bash

HELP="
Restores example data to data directory
Resets mongodb data and imports data from file system into mongodb.

Usage

Run it from the /src directory in the repo.

./import.sh [test|prod]
./import.sh
    Test mode

./import.sh prod
    Production mode

"

flaskdebug=""
flasktest=""

while [ ! -z "$1" ]; do
    if [[ "$1" == "--help" ]]; then
        printf "$HELP\n"
        exit 0
    fi
    if [[ "$1" == "prod" ]]; then
        flaskdebug=""
        flasktest=""
        shift
    elif [[ "$1" == "test" ]]; then
        flaskdebug="--debug"
        flasktest="test"
        shift
    else
        echo "unrecognized argument '$1'"
        shift
    fi
done


cd ..
repodir="`pwd`"

echo "Removing old data ..."
rm -rf data

echo "Copying fresh example data ..."
cp -r exampledata data

cd src

export repodir
export flasktest
export flaskdebug

echo "Filling mongodb collections ..."
python3 pure3d/import.py
echo "Done"
