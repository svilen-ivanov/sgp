#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

VIDEO=output/video
AUDIO=output/audio
#ffmpeg \
#  -i $VIDEO/Description.mp4 \
#  -i $AUDIO/Description.flac \
#   -map '0' -map '1' \
#   -threads 4 \
#   -vcodec copy -acodec copy -shortest \
#   Description.mkv
#

ffmpeg -i $VIDEO/Description.mp4 \
       -i $AUDIO/Description.flac \
  -filter_complex \
  " [0] setpts='PTS-STARTPTS +

gte(T,2)*(2.4800000000000004/TB)+
gte(T,4)*(2.119999999999999/TB)+
gte(T,4.016666666666667)*(6.383333333333333/TB)

    ' [v1] ;
    [v1] select=between(t\,0\,23) [vout]
  " \
  -map '[vout]' -map '1' \
  -vsync cfr \
  -threads 4 \
  -vcodec libx264 \
  -preset ultrafast \
  -acodec copy \
  -y \
  Description.mkv
