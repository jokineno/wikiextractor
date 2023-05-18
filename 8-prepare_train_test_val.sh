#!/bin/bash

set -x
echo "Copy training data for training"
mkdir -p training
mkdir -p holdout

METADATA="metadata.json"

cp -v $METADATA ./holdout/metadata.json
cp -v $METADATA ./training/metadata.json

python prepare_train_test_val.py \
  --holdout_dir ./holdout \
  --training_dir ./training \
  --metadata metadata.json \
  --citations final_citation_data_filtered.json

echo "Running data_validator to holdout and training sets."
echo "##############Running data validator to holdout##############"
python data_validator.py --citations holdout/data.json --metadata holdout/metadata.json
echo "##############Running data validator to training##############"
python data_validator.py --citations training/data.json --metadata training/metadata.json
echo "Done"
