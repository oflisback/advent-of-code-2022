#/bin/bash

if [ "$1" = "" ]
then
  echo "Usage: $0 <slack|modelon|kodsnack|podsnack> [year]"
  exit
fi

declare -A list_ids
list_ids=(["slack"]=1899697 ["modelon"]=1148895 ["kodsnack"]=145301 ["podsnack"]=143527)
list_id="${list_ids[$1]}"

if [ -z $list_id ]
then
  echo "List with name $1 not found"
  exit
fi

year=$2
if [ -z $year ]
then
  year=$(date +"%Y")
fi

session_row=$(cat .env)
session_array=(${session_row//=/ })
session_cookie=${session_array[1]}

mkdir -p "./highscore-lists"
output_path="$(pwd)/highscore-lists/${1}-${year}.json"
curl -s --cookie "session=${session_cookie}" \
  "https://adventofcode.com/${year}/leaderboard/private/view/${list_id}.json" \
  --output "${output_path}"
echo "Saved to ${output_path}"
