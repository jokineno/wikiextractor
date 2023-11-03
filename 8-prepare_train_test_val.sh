#!/bin/bash

set -x
echo "Copy training data for training"
mkdir -p -v training
mkdir -p -v holdout

METADATA="metadata.json"

cp -v $METADATA ./holdout/metadata.json
cp -v $METADATA ./training/metadata.json

if [ -z "$1" ]
 then
   echo "################NO SAMPLE SIZE GIVEN. FULL DATA################"
  python prepare_train_test_val.py \
    --holdout_dir ./holdout \
    --training_dir ./training \
    --metadata metadata.json \
    --citations final_citation_data_filtered.json
else
  SAMPLE_SIZE="$1"
  echo "Running with sample size $SAMPLE_SIZE"
  python prepare_train_test_val.py \
    --holdout_dir ./holdout \
    --training_dir ./training \
    --metadata metadata.json \
    --citations final_citation_data_filtered.json \
    --sample_size $SAMPLE_SIZE
fi

SAMPLE_SIZE="$1"

python prepare_train_test_val.py \
  --holdout_dir ./holdout \
  --training_dir ./training \
  --metadata metadata.json \
  --citations final_citation_data_filtered.json \
  --sample_size $SAMPLE_SIZE

echo "Running data_validator to holdout and training sets."
echo "##############Running data validator to holdout##############"
python data_validator.py --citations holdout/data.json --metadata holdout/metadata.json
echo "##############Running data validator to training##############"
python data_validator.py --citations training/data.json --metadata training/metadata.json
echo "Done"
