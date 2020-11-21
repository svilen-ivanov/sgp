#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

VIDEO=output/video
AUDIO=output/audio
NAME=BruteForce

ffmpeg -i $VIDEO/$NAME.mp4 \
       -i $AUDIO/$NAME.flac \
       -i $VIDEO/BruteForceTitle.mp4 \
  -filter_complex \
  "     [0] setpts=2*PTS [v1] ;
  [v1] select=between(t\,0\,15) [v2] ;
  [2][v2] concat=n=2:v=1 [v3] ;
  [v3] select=between(t\,0\,15) [vout]
  " \
  -map '[vout]' -map '1' \
  -vsync cfr \
  -threads 4 \
  -vcodec libx264 \
  -acodec copy \
  -y \
  $NAME.mkv
