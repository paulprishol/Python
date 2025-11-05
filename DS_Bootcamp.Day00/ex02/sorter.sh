#!/bin/sh

INPUT="../ex01/hh.csv"
OUTPUT="./hh_sorted.csv"

head -n 1 $INPUT > $OUTPUT
tail -n +2 $INPUT | sort -t "," -k 2 -k 1 >> $OUTPUT

echo "Файл hh.csv отсортирован в hh_sorted.csv"