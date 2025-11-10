#!/bin/sh

INPUT="../ex00/hh.json"
OUTPUT="./hh.csv"
FILTER="./filter.jq"

echo "\"id\",\"created_at\",\"name\",\"has_test\",\"alternate_url\"" > $OUTPUT

jq -rf $FILTER $INPUT >> $OUTPUT

echo "Данные из json преобразованы в csv"
