"""
This script combines direct citations data and 
hard negatives citations. 

Hard negatives are the ones where query paper P1 cites paper P2 and P2 cites P3 but P1 does not cite P3.
There is basically some indirect relationship between P1 and P3. 
"""

import json 
from tqdm import tqdm

from common import setup_logging
import sys
log_file = sys.argv[0] + ".log"
logger = setup_logging(log_output=log_file)

def read_files():
    logger.info("Reading direct_citations.json")
    with open("direct_citations.json", "r") as f:
        direct_data = json.load(f)
    
    with open("hard_negatives.json", "r") as f:
        hard_negatives = json.load(f)

    return direct_data, hard_negatives


def combine_citations():
    direct, hard = read_files()
    for key in tqdm(direct):
        direct[key].update(hard[key])
    return direct


if __name__ == "__main__":
    metadata = combine_citations()
    output_path = "final_citation_data.json"
    with open(output_path, "w") as f:
        f.write(json.dumps(metadata))

    print(f"Wrote metadata to {output_path}")
