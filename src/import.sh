#!/bin/bash

HELP="
Restores example data to data directory
Resets mongodb data and imports data from file system into mongodb.

Usage

Run it from the /src directory in the repo.

./import.sh [test|prod] [viewers] [content]
./import.sh
    Test mode

./import.sh prod
    Production mode

Pass tasks to indicate what should be imported:

viewers
    Inspects the viewers.yaml file and the installed viewers in the
    static directory in order to configure the supported viewers

content
    Imports content from the file system and fills mongodb tables
    accordingly
"

flaskdebug=""
flasktest=""

doviewers="x"
docontent="x"

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
    elif [[ "$1" == "viewers" ]]; then
        doviewers="v"
    elif [[ "$1" == "content" ]]; then
        docontent="v"
    else
        echo "unrecognized argument '$1'"
        shift
    fi
done


cd ..
repodir="`pwd`"

if [[ "$doviewers" == "v" ]]; then
    cd src

    export repodir
    export flasktest
    export flaskdebug

    echo "Entering viewer config in mongodb"
    python3 pure3d/import.py viewers
    echo "Done"

elif [[ "$docontent" == "v" ]]; then
    echo "Removing old data ..."
    rm -rf data

    echo "Copying fresh example data ..."
    cp -r exampledata data

    cd src

    export repodir
    export flasktest
    export flaskdebug

    echo "Filling mongodb collections ..."
    python3 pure3d/import.py content
    echo "Done"
fi
