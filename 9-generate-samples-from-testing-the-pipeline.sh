#!/bin/bash

set -x
SAMPLE_SIZE=100

echo "Generating samples with sample size $SAMPLE_SIZE"
mkdir -p training_demo
python prepare_train_test_val.py --sample_size $SAMPLE_SIZE --output_path training_demo
python

echo "Done"