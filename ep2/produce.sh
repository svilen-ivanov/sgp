#!/usr/bin/env bash

VIDEO_OUTPUT=./
rm -f output.mkv
ffmpeg \
  -i $VIDEO_OUTPUT/TitleScreen.mkv \
  -i $VIDEO_OUTPUT/Description.mkv   \
  -i $VIDEO_OUTPUT/BruteForce.mkv \
  -i $VIDEO_OUTPUT/Greedy.mkv \
  -i $VIDEO_OUTPUT/OptSubstr.mkv \
  -i $VIDEO_OUTPUT/Algo.mkv \
  -i $VIDEO_OUTPUT/DynamicProgramming.mkv \
  -i $VIDEO_OUTPUT/MinChangeStepByStep.mkv \
  -filter_complex \
  '[0:0] [0:1] [1:0] [1:1] [2:0] [2:1] [3:0] [3:1] [4:0] [4:1] [5:0] [5:1] [6:0] [6:1] [7:0] [7:1]
   concat=n=8:v=1:a=1 [v] [am] ;
   amovie=bg_long.flac,volume=0.1 [bg_track] ;
   [am] amerge=inputs=1 [a_stereo] ;
   [a_stereo]loudnorm[a_stereo_norm] ;
   [a_stereo_norm]volume=2[aamp] ;
   [aamp][bg_track]amix=duration=first[a]' \
   -map '[v]' -map '[a]' \
   -threads 4 \
   -vcodec libx264 -acodec libopus -shortest \
  output.mkv
