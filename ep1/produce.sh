#!/usr/bin/env bash

#VIDEO_OUTPUT=media/videos/scene/480p15
VIDEO_OUTPUT=media/videos/scene/2160p60
rm -f output.mkv
ffmpeg \
  -i $VIDEO_OUTPUT/TitleScreen.mp4 \
  -i $VIDEO_OUTPUT/SortingScene.mp4 \
  -i $VIDEO_OUTPUT/StudentsSortingScene.mp4 \
  -i $VIDEO_OUTPUT/DivideAndConquer.mp4 \
  -i $VIDEO_OUTPUT/Complexity.mp4 \
  -i $VIDEO_OUTPUT/MainAlgo.mp4 \
  -i $VIDEO_OUTPUT/MergeSort.mp4 \
  -i $VIDEO_OUTPUT/Final.mp4 \
  -filter_complex \
  '[0:0] [0:1] [1:0] [1:1] [2:0] [2:1] [3:0] [3:1] [4:0] [4:1] [5:0] [5:1] [6:0] [6:1] [7:0] [7:1]
   concat=n=8:v=1:a=1 [v] [am] ;
   amovie=bg_7min.flac,volume=0.03 [bg_track] ;
   [am]amerge=inputs=1 [a_stereo] ;
   [a_stereo]volume=1.2[aamp] ;
   [aamp][bg_track]amix=duration=first[a]' \
   -map '[v]' -map '[a]' \
   -threads 4 \
   -vcodec libx264 -acodec libopus -shortest \
  output.mkv
# -filter_complex "amovie=bg.flac:loop=0,volume=0.03[audio];[0:a]volume=1.2[sa];[sa][audio]amix[fa]" \

# -map 0:v -map [fa] \
# out.mp4


