#!/bin/bash

HELP="""
Reduces quality of images in the media directories
Do ./install.sh from the same directory first
"""

cd data/projects
for f in ./*/editions/*/articles/media/*.jpg ./*/editions/*/articles/media/*.jpeg  ./*/editions/*/articles/media/*.png
    do
    mogrify -resize 50% $f
    done