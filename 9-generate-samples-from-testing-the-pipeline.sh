#!/bin/bash

set -x
SAMPLE_SIZE=100
INFERENCE_SAMPLE_SIZE=55

echo "Generating samples with sample size $SAMPLE_SIZE"
mkdir -p training_demo
python prepare_train_test_val.py --sample_size $SAMPLE_SIZE --output_path training_demo
python filter_metadata_and_citations.py \
  --metadata metadata.json \
  --citations final_citation_data_filtered.json \
  --idlist training_demo/all.txt \
  --output_dir training_demo


mkdir -p inference_demo
python generate_data_for_inference.py \
  --output_dir inference_demo \
  --metadata metadata.json \
  --blacklist training_demo/all.txt \
  --sample_size $INFERENCE_SAMPLE_SIZE
echo "Done"