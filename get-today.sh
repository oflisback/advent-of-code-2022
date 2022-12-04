#/bin/bash

dayNumber=$(date +'%-d')
targetDir=./input/$dayNumber
echo $targetDir
mkdir -p $targetDir
aocd > $targetDir/input.txt
