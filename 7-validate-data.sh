#!/bin/bash

set -x

echo "Validating data..."
python data_validator.py --citations final_citation_data_filtered.json --metadata metadata.json
echo "Done"