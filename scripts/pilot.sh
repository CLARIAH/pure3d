#!/bin/bash

HELP="""
Run PILOT website

Usage

Run it from the /scripts directory in the repo.

./pilot.sh name ['prod'] [host:port]
    Run named pilot in debug mode.
    An environment variable PILOT_MODE will be set to dev or prod
    default dev, if 'prod' is passed: prod

    You can also specify a host:port.
"""

scriptdir=`pwd`
cd ../pilots
pilotdir=`pwd`

if [[ "$1" == "" ]]; then
    echo $HELP
    echo ""
    echo "Error in calling this program!"
    echo "Missing pilot name"
    exit 1
fi

pilotname="$1"
shift


if [[ "$1" == "prod" ]]; then
    PILOT_MODE="prod"
    shift
else
    PILOT_MODE="dev"
fi
if [[ "$1" == "" ]]; then
    PILOT_HOST="127.0.0.1"
    PILOT_PORT="5000"
else
    PILOT_HOST="$1"
    shift
    if [[ "$1" == "" ]]; then
        PILOT_PORT="5000"
    else
        PILOT_PORT="$1"
    fi
fi

if [[ ! -d "$pilotname" ]]; then
    echo "Pilot '$pilotname' does not exist"
    exit 1
fi

cd "$pilotname"
export PILOT_MODE
export PILOT_HOST
export PILOT_PORT

# start server

if [[ -f "cmd.sh" ]]; then
    ./cmd.sh &
else
    flask --debug --app app:app run --host $PILOT_HOST --port $PILOT_PORT &
fi
pid=$!
pgid=`ps -o pgid= $pid | grep -o '[0-9]*'`

sleep 1

# start browser

if [[ -f "url.txt" ]]; then
    url=`cat url.txt`
else
    url="http://$PILOT_HOST:$PILOT_PORT/"
fi

python3 "$scriptdir/browser.py" "$url"
trap "kill -- -$pgid" SIGINT
echo "server runs as process $pid with parent $pgid"
wait "$pid"
