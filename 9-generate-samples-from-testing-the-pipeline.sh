#!/bin/bash

echo "Generating samples for training"
python sample-data.py

cp -v sample.json ./training/data-sample.json


echo "Done"