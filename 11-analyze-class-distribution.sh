#/bin/bash 

set -x 

echo "Starting to analyze class distribution of holdout dataset"
python analyze-class-distribution.py \
  --metadata ./holdout/metadata.json \
  --citation ./holdout/data.json

echo "Done"
