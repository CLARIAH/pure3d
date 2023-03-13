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

cd ../pilots
pytest