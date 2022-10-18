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

--mongostart
    Only start the mongodb server

--mongostop
    Only stop the mongodb server

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
MONGO_DATA
    Path to the directory where mongodb stores its data.
    It is recommended that the data dir is not anywhere
    inside the clone of this repository.
    A good location is in "mongodb" inside DATA_DIR.
MONGO_IP
    IP address that mongodb should bind to
MONGO_PORT
    Port where mongodb is listening.
"

########################################################################
# default values for variables
# that have not but should be defined by the environment
# before calling this script
#
SECRET_FILE_DEFAULT="/opt/web-apps/pure3d.secret"
DATA_DIR_DEFAULT="/var/data/pure3d"
MONGO_IP_DEFAULT="0.0.0.1"
MONGO_PORT_DEFAULT="27017"
MONGO_DATA_DEFAULT="/var/data/pure3d/mongodb"
#
# end of default values
########################################################################

flaskdebug=""
flasktest=""
flaskhost="0.0.0.0"
# flaskhost="127.0.0.1"
flaskport="8000"
browse="x"
commandonly=""

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
    elif [[ "$1" == "--mongostart" ]]; then
        commandonly="mongostart"
        shift
    elif [[ "$1" == "--mongostop" ]]; then
        commandonly="mongostop"
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
if [[ -z ${MONGO_IP+x} ]]; then
    MONGO_IP="$MONGO_IP_DEFAULT"
    export MONGO_IP
fi
if [[ -z ${MONGO_PORT+x} ]]; then
    MONGO_PORT="$MONGO_PORT_DEFAULT"
    export MONGO_PORT
fi
if [[ -z ${MONGO_DATA+x} ]]; then
    MONGO_DATA="$MONGO_DATA_DEFAULT"
    export MONGO_DATA
fi

function mongostart {
    if [[ `ps aux | grep -v grep | grep mongod` ]]; then
        :
    else
        if [[ "$flasktest" == "test" ]]; then
            logargs=""
        else
            logargs="--syslog "
        fi
        fork=" --fork"
        verbose=""
        if [[ "$commandonly" == "mongostart" ]]; then
            fork=""
            logargs=""
            verbose="-v"
            echo "mongod "$verbose" --bind_ip "$MONGO_IP" --ipv6 --port "$MONGO_PORT" "$logargs"--dbpath "$MONGO_DATA"$fork"
        fi
        mongod "$verbose" --bind_ip "$MONGO_IP" --ipv6 --port "$MONGO_PORT" "$logargs" --dbpath "$MONGO_DATA"$fork
    fi
}

function mongostop {
    pid=`ps aux | grep -v grep | grep mongod | awk '{print $2}'`
    if [[ "$pid" == "" ]]; then
        :
    else
        kill $pid
        echo "mongo daemon stopped"
    fi
}


if [[ "$commandonly" != "" ]]; then
    if [[ "$commandonly" == "mongostart" ]]; then
        mongostart
        exit
    elif [[ "$commandonly" == "mongostop" ]]; then
        mongostop
    fi
    exit
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

mongostart

if [[ "$browse" == "v" ]]; then
    flask $flaskdebug run --host $flaskhost --port $flaskport &
    pid=$!
    sleep 1
    python3 "$repodir/scripts/browser.py" http://$flaskhost:$flaskport
    trap "kill $pid" SIGINT
    echo "flask runs as process $pid"
    wait "$pid"
    mongostop
else
    flask $flaskdebug run --host $flaskhost --port $flaskport
fi
