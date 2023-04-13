#!/bin/bash

set -x

echo "Combining citations (direct citations and hard negatives) generating final_citation_data.json"
python combine_citations.py
echo "Done."