#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

VIDEO=output/video
AUDIO=output/audio
NAME=DynamicProgramming

ffmpeg -i $VIDEO/$NAME.mp4 \
       -i $AUDIO/$NAME.flac \
    -filter_complex \
  " [0] setpts='PTS-STARTPTS +
  gte(T,23)*(3/TB)

    ' [vout]
  " \
  -map '[vout]' -map '1' \
  -vsync cfr \
  -threads 4 \
  -vcodec libx264 \
  -acodec copy \
  -y \
  $NAME.mkv
