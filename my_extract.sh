#!/bin/bash 

if [[ $* == *--debug* ]]
then 
  echo "Debugging"
  python -m wikiextractor.WikiExtractor ../data/debug.xml -ns ns0 --json --no-templates --output debug_output
  echo "Done debugging"
  exit 1
fi


if [[ ! $* == *--test* ]]
then
  echo "Starting to extract..."
  python -m wikiextractor.WikiExtractor ../data/fiwiki-20220301-pages-articles-multistream.xml -ns ns0 --json --no-templates
  echo "Done"
else
  echo "TESTING EXTRACT...."
  python -m wikiextractor.WikiExtractor ../data/fiwiki-20220301-pages-articles-multistream.xml -ns ns0 --json  --no-templates --output test
  echo "Done"


fi
