#!/bin/bash

HELP="""
Reduces quality of images in the media directories
Do ./install.sh from the same directory first
"""

cd ../data/projects
for f in ./2/editions/2/articles/media/*.JPG ./2/editions/2/articles/media/*.jpeg  ./2/editions/2/articles/media/*.png 
    do
    mogrify -resize 50% $f
    done