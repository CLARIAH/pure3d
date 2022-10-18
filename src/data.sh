#!/bin/bash

datasource=~/github/clariah/pure3d/data
dataroot=/var/data/pure3d

HELP="
Copies data folder from $datasource into $dataroot 

If $dataroot does not exist, you need to create it yourself first.

You might need sudo rights.
After creating, make it write accessible to the normal user.
E.g.

sudo mkdir -p $dataroot
chmod u+rwx $dataroot
"

while [ ! -z "$1" ]; do
    if [[ "$1" == "--help" ]]; then
        printf "$HELP\n"
        exit 0
    fi
done

if [[ ! -e "$dataroot" ]]; then
    printf "No directory $dataroot."
    printf "$HELP"
    exit 1
fi

cd $datasource

for d in *
do
    echo "$d"
    cp -f -r "$d" "$dataroot/$d"
done
