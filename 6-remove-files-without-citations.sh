#!/bin/bash


echo "Starting to clean and finalize data..."
python clean_data.py --citations final_citation_data.json
echo "Done"