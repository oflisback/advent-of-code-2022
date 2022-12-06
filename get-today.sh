#/bin/bash

dayNumber=$(date +'%-d')
targetDir=./src/$dayNumber
echo $targetDir
mkdir -p $targetDir
aocd > $targetDir/input.txt
cat $targetDir/input.txt
wc -l $targetDir/input.txt
