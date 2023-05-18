#!/bin/bash

set -x

echo "Starting to generate citation data"
echo "For the data the task is to choose 1000 query papers and for each 5 cited papers and 25 uncited papers."
echo "The inference task is to predict cited papers higher than uncited papers"

SAMPLE_SIZE=$1

mkdir -p scidocs_citation_data
python generate-scidocs-citation-data.py \
  --metadata metadata.json \
  --citations final_citation_data_filtered.json \
  --is_test_val test \
  --sample_size $SAMPLE_SIZE

echo "Done"