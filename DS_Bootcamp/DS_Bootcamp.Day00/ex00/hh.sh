#!/bin/sh

if [ -z "$1" ]; then
  echo "Ошибка: укажите название вакансии в качестве аргумента"
  echo "Пример: ./get_vacancies.sh \"специалист по данным\""
  exit 1
fi

OUTPUT="./hh.json"
VAC_VALUE="20"

curl -H 'User-Agent: api-test-agent' -G "https://api.hh.ru/vacancies?text=$1&page=0&per_page=$VAC_VALUE" | jq > $OUTPUT

echo "Данные по вакансии '$1' сохранены в hh.json"
