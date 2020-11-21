#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

export PYTHONPATH=../

QUALITY=-ql
#QUALITY=-qk
#rm -rf media
manim scenes/title_scene.py TitleScreen $QUALITY
manim scenes/description.py Description $QUALITY
manim scenes/brute_force.py BruteForce $QUALITY
manim scenes/greedy.py Greedy $QUALITY
manim scenes/dynamic_programming.py DynamicProgramming $QUALITY
manim scenes/opt_substr.py OptSubstr $QUALITY
manim scenes/algo.py Algo $QUALITY
manim scene.py MinChangeStepByStep $QUALITY
