#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

VIDEO=output/video
AUDIO=output/audio
NAME=Greedy

ffmpeg -i $VIDEO/$NAME.mp4 \
       -i $AUDIO/$NAME.flac \
       -i $VIDEO/GreedyTitle.mp4 \
  -filter_complex \
  "
  [2] select=between(t\,0\,10) [v2] ;
  [v2] setpts='PTS-STARTPTS +
    gte(T,1)*(5/TB)
    '
    [v2a] ;
    [0] setpts='PTS-STARTPTS +
    gte(T,1)*(5/TB)
    '
    [v2b] ;
    [v2a][v2b] concat=n=2:v=1 [vconcat] ;
    [vconcat] select=between(t\,0\,33) [vout]
  " \
  -map '[vout]' -map '1' \
  -vsync cfr \
  -threads 4 \
  -vcodec libx264 \
  -preset ultrafast \
  -acodec copy \
  -y \
  $NAME.mkv
