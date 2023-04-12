#!/bin/bash

echo "Combining citations (direct citations and hard negatives) generating final_citation_data.json"
pytho combine_citations.py
echo "Done."