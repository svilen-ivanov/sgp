#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

VIDEO=output/video
AUDIO=output/audio
NAME=BruteForce

ffmpeg -i $VIDEO/$NAME.mp4 \
       -i $AUDIO/$NAME.flac \
  -filter_complex \
  "
    [0] setpts=3.0*PTS [v1] ;
    [v1] select=between(t\,0\,14.5) [vout]
  " \
  -map '[vout]' -map '1' \
  -vsync cfr \
  -threads 4 \
  -vcodec libx264 \
  -preset ultrafast \
  -acodec copy \
  -y \
  $NAME.mkv
