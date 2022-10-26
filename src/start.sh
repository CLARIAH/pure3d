#!/bin/bash

HELP="
Run Pure3D webapp, optionally start a browsing session as well.

Usage

Run it from the /src directory in the repo.

./start.sh [test|prod]
./start.sh
    Test mode

./start.sh prod
    Production mode

Options:

--browse
    Start a browsing session after starting the app.

"

flaskdebug=""
flasktest=""
flaskhost="0.0.0.0"
flaskport="8000"
browse="x"

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
    elif [[ "$1" == "--browse" ]]; then
        browse="v"
        shift
    else
        flaskport="$1"
        shift
        break
    fi
done


cd ..
repodir="`pwd`"
cd src/pure3d

export flasktest
export flaskdebug
export flaskport
export repodir
export FLASK_APP=index

if [[ "$browse" == "v" ]]; then
    flask $flaskdebug run --host $flaskhost --port $flaskport &
    pid=$!
    sleep 1
    python3 "$repodir/scripts/browser.py" http://$flaskhost:$flaskport
    trap "kill $pid" SIGINT
    echo "flask runs as process $pid"
    wait "$pid"
else
    flask $flaskdebug run --host $flaskhost --port $flaskport &
    pid=$!
    trap "kill $pid" SIGTERM
    wait "$pid"
fi
