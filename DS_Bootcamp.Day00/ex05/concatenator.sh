#!/bin/sh

OUTPUT="./hh_positions.csv"

echo '"id","created_at","name","has_test","alternate_url"' > $OUTPUT

for FILE in *.csv;
do
  if [ "$FILE" = $(basename "$OUTPUT") ]; then
     continue
  fi
  tail -n +2 $FILE >> $OUTPUT
done

echo "Данные сохранены в hh_positions.csv"