#!/bin/bash

HELP="
Ship Pure3D app.

Usage

Run it from the /scripts directory in the repo.

./ship.sh dev commit_message

It will write commit data to

src/pure3d/control/commit.txt

so that the app can display version info on the screen.
"

mode=""
msg=""

while [ ! -z "$1" ]; do
    if [[ "$1" == "--help" ]]; then
        printf "$HELP\n"
        exit 0
    fi
    if [[ "$1" == "dev" ]]; then
        mode="dev"
        shift
    else
        if [[ "$mode" != "" ]]; then
            msg="$1"
            shift
        else
            echo "unrecognized argument: '$1'"
            shift
        fi
    fi
done

if [[ "$mode" == "" ]]; then
    printf "$HELP\n"
    echo "no mode given"
    exit 1
fi

if [[ "$msg" == "" ]]; then
    printf "$HELP\n"
    echo "no commit_message given"
    exit 1
fi

git add --all .
git commit -m "$msg"
git push origin main
git log -n 1 --pretty=reference --abbrev-commit --date=iso > version.txt
