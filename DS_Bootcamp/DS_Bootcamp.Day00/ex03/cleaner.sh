#!/bin/sh

INPUT="../ex02/hh_sorted.csv"
OUTPUT="./hh_positions.csv"

head -n 1 $INPUT > $OUTPUT
tail -n +2 $INPUT | awk -F '",' '{
    pos = "-"
    if ($3 ~ /[Jj]unior/) pos = "Junior"
    if ($3 ~ /[Mm]iddle/) pos = (pos == "-" ? "Middle" : pos "/Middle")
    if ($3 ~ /[Ss]enior/) pos = (pos == "-" ? "Senior" : pos "/Senior") 
    $3 = "\"" pos "\""
    print $1 "\"," $2 "\"," $3 "," $4
}'>> $OUTPUT

echo "Информация сохранена в файле hh_positions.csv"