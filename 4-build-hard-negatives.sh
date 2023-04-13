#!/bin/bash

set -x

echo "Building hard negatives.."
python build_hard_negatives.py
echo "Done"

