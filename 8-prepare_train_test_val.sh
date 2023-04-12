#!/bin/bash

set -x 

echo "starting to prepare train test val split"
python prepare_train_test_val.py
echo "Done."