#!/bin/bash

set -x

echo "Building title2id and id2title mappings"
python build_title_to_id_map_from_index_file.py
echo "Done"