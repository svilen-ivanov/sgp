#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

VIDEO=output/video
AUDIO=output/audio
ffmpeg \
  -i $VIDEO/TitleScreen.mp4 \
  -i $AUDIO/TitleScreen.flac \
   -map '0' -map '1' \
   -threads 4 \
   -vcodec copy -acodec copy \
    -shortest \
    -y \
   TitleScreen.mkv
