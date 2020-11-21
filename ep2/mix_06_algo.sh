#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

VIDEO=output/video
AUDIO=output/audio
NAME=Algo

ffmpeg -i $VIDEO/$NAME.mp4 \
       -i $AUDIO/$NAME.flac \
    -filter_complex \
  " [0] setpts='PTS-STARTPTS +
gte(T,16)*(10/TB) +
gte(T,23)*(3/TB)
    ' [v1] ;
      [v1] select=between(t\,0\,64) [vout]
  " \
  -map '[vout]' -map '1' \
  -vsync cfr \
  -threads 4 \
  -vcodec libx264 \
  -acodec copy \
  -y \
  $NAME.mkv
