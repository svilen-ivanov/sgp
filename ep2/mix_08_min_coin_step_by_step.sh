#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

VIDEO=output/video
AUDIO=output/audio
NAME=MinChangeStepByStep

ffmpeg -i $VIDEO/$NAME.mp4 \
       -i $AUDIO/$NAME.flac \
    -filter_complex \
  " [0] setpts='PTS-STARTPTS +
  gte(T,13)*(18/TB)
    ' [vout] ;
  " \
  -map '[vout]' -map '1' \
  -vsync cfr \
  -threads 4 \
  -vcodec libx264 \
  -preset ultrafast \
  -acodec copy \
  -y \
  $NAME.mkv
