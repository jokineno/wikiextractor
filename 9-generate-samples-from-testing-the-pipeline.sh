#!/bin/bash

set -x
SAMPLE_SIZE=100

echo "Generating samples with sample size $SAMPLE_SIZE"
mkdir -p training_demo
python prepare_train_test_val.py --sample_size $SAMPLE_SIZE --output_path training_demo
python filter_metadata_and_citations.py \
  --metadata metadata.json \
  --citations final_citation_data.json \
  --idlist training_demo/all.txt \
  --output_dir training_demo
echo "Done"