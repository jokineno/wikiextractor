#!/bin/bash 

echo "copy training data for specter training"


mkdir -p training

cp -v metadata.json ./training/
cp -v final_citation_data.json ./training/data.json
python prepare_train_test_val.py

echo "Done"