"""
This script combines direct citations data and 
hard negatives citations. 

Hard negatives are the ones where query paper P1 cites paper P2 and P2 cites P3 but P1 does not cite P3.
There is basically some indirect relationship between P1 and P3. 
"""

import json 
from tqdm import tqdm

def read_files():
    with open("direct_citations.json", "r") as f:
        direct_data = json.load(f)
    
    with open("hard_negatives.json", "r") as f:
        hard_negatives = json.load(f)

    return direct_data, hard_negatives

def combine():
    metadata = {}
    direct, hard = read_files()

    for key in tqdm(direct):
        direct[key].update(hard[key])


    return direct

import random
metadata = combine()
output_path = "final_citation_data.json"
with open(output_path, "w") as f:
    f.write(json.dumps(metadata))
print(f"Wrote metadata to {output_path}")

print("Generating sample with 100 keys")
sample = {key: metadata[key] for key in random.sample(list(metadata),100)}
sample_path = "sample.json"
with open(sample_path, "w") as f:
    f.write(json.dumps(sample))

print(f"Wrote metadata to {sample_path}")
