#/bin/bash

dayNumber=$(date +'%-d')
targetDir=./src/$dayNumber
echo $targetDir
mkdir -p $targetDir
aocd > $targetDir/input.txt
