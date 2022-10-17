#!/bin/bash

HELP="
Run Pure3D webapp, optionally start a browsing session as well.

Usage

Run it from the /scripts directory in the repo.

./pure3d.sh test
./pure3d.sh
    Test mode

./pure3d.sh prod
    Production mode

Options:

--browser
    Start a browsing session after starting the app.

Requirements
------------

This script can be started from any directory,
and it will cd to the local clone of the pure3d repo.

A number of environment variables will
be set to hard-wired default values, unless they are defined
by the environment.
These values point to
files and directories with expected content, see below.

When the python code starts,
it will first check whether these environmnet variables
are defined, and secondly whether the things they point to
exist. 

If all is well, the flask app will be started.

Here is the list:

SECRET_FILE
    Location of a file with a random string used
    to encrypt sessions.

DATA_DIR
    Path to the directory that contains the file-based
    data store of Pure3D.
    The data store must have a structure defined by Pure3d,
    an example is in this repo under /data.
    It is recommended that the data dir is not anywhere
    inside the clone of this repository.
"

########################################################################
# default values for variables
# that have not but should be defined by the environment
# before calling this script
#
SECRET_FILE_DEFAULT="/opt/web-apps/pure3d.secret"
DATA_DIR_DEFAULT="/var/data/pure3d"
#
# end of default values
########################################################################

flaskdebug=""
flasktest=""
flaskhost="0.0.0.0"
# flaskhost="127.0.0.1"
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

# set several variables to default values if not supplied
# by the environment 
if [[ -z ${SECRET_FILE+x} ]]; then
    SECRET_FILE="$SECRET_FILE_DEFAULT"
    export SECRET_FILE
fi
if [[ -z ${DATA_DIR+x} ]]; then
    DATA_DIR="$DATA_DIR_DEFAULT"
    export DATA_DIR
fi

srcdir="${0%/*}"
cd "$srcdir/.."
repodir="`pwd`"
cd "src/pure3d/control"
printf "Working in repo $repodir\n"


export flasktest
export flaskdebug
export flaskport
export repodir

if [[ "$browse" == "v" ]]; then
    flask $flaskdebug run --host $flaskhost --port $flaskport &
    pid=$!
    sleep 1
    python3 "$repodir/scripts/browser.py" http://$flaskhost:$flaskport
    trap "kill $pid" SIGINT
    echo "flask runs as process $pid"
    wait "$pid"
else
    flask $flaskdebug run --host $flaskhost --port $flaskport
fi
