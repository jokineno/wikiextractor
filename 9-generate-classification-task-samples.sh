#!/bin/bash

set -x
SAMPLE_SIZE=100
INFERENCE_SAMPLE_SIZE=55


echo "Generating samples with sample size $SAMPLE_SIZE"
mkdir -p training_demo
mkdir -p holdout_demo

python prepare_train_test_val.py \
  --sample_size $SAMPLE_SIZE \
  --metadata metadata.json \
  --citations final_citation_data_filtered.json \
  --training_dir training_demo \
  --holdout_dir holdout_demo \

python filter_metadata_and_citations.py \
  --metadata training_demo/metadata.json \
  --citations training_demo/data.json \
  --idlist training_demo/all.txt \
  --output_dir training_demo


mkdir -p inference_demo
python generate_data_for_inference.py \
  --output_dir inference_demo \
  --citations holdout_demo/data.json \
  --metadata metadata.json \
  --sample_size $INFERENCE_SAMPLE_SIZE
echo "Done"