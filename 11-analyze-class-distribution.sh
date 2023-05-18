#/bin/bash 

set -x 

echo "Starting to analyze class distribution"
python analyze-class-distribution.py --metadata metadata.json 
echo "Done"
