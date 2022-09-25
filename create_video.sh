#!/bin/bash
find ./generations/new -mindepth 2 -maxdepth 2 -type d | xargs -i  ffmpeg -framerate 25 -i {}/counts%d.jpg -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p {}/a.mp4
