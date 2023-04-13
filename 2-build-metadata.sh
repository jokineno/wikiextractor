#!/bin/bash

set -x

echo "Building metadata from wiki articles"
python build_metadata.py
echo "Done"