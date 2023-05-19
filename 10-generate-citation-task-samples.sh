#!/bin/bash

set -x

echo "Starting to generate citation data"
echo "For the data the task is to choose 1000 query papers and for each 5 cited papers and 25 uncited papers."
echo "The inference task is to predict cited papers higher than uncited papers"

SAMPLE_SIZE=$1
if [ -z "$1" ]; then
    echo "No argument was provided."
    exit 1
else
    echo "Argument was provided: $1"
fi


if [[ $1 =~ ^[0-9]+$ ]]; then
    echo "Argument is numeric: $1"
else
    echo "Argument is not numeric or not provided."
    exit 1
fi


mkdir -p holdout/citation/
python generate-scidocs-citation-data.py \
  --metadata metadata.json \
  --citations holdout/data.json \
  --sample_size $SAMPLE_SIZE

echo "Done"
