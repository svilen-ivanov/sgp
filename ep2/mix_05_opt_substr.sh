#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

VIDEO=output/video
AUDIO=output/audio
NAME=OptSubstr

ffmpeg -i $VIDEO/$NAME.mp4 \
       -i $AUDIO/$NAME.flac \
  -filter_complex \
  " [0] setpts='PTS-STARTPTS +
gte(T,0)*(1/TB)+
gte(T,5)*(3/TB)
    ' [v1] ;
    [v1] select=between(t\,0\,14) [vout]
  " \
  -map '[vout]' -map '1' \
  -vsync cfr \
  -threads 4 \
  -vcodec libx264 \
  -acodec copy \
  -y \
  $NAME.mkv
