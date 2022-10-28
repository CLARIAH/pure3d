#!/bin/bash

HELP="""
Reduces quality of audio/video files in the media directories
Do ./install.sh from the same directory first
"""
 cd ../data/projects

for f in ./*/editions/*/articles/media/*.mp3 ./*/editions/*/articles/media/*.mp4  ./*/editions/*/articles/media/*.wav
    do
    ffmpeg -i $f -b:a 96k -map a $f
    done