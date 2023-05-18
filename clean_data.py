import copy
import sys

import json
import argparse
import tqdm
from common import setup_logging
from collections import Counter
log_file = sys.argv[0] + ".log"
logger = setup_logging(log_output=log_file)


def main(citations_path):
    logger.info("Reading {}".format(citations_path))
    with open(citations_path, "r") as f:
        citations = json.load(f)
    logger.info("Read {}. Item count {}".format(citations_path, len(citations)))
    citations_filtered = copy.deepcopy(citations)
    master_counter = Counter()
    all_citations = len(citations)
    running_count = 0
    for query, related_citations in citations.items():
        running_count += 1
        if running_count % 1000 == 0:
            logger.info("Handling {}/{}".format(running_count, all_citations))

        counter = Counter()
        counts = [v['count'] for _, v in related_citations.items()]
        counter.update(counts)

        count_5 = counter.get(5)
        count_1 = counter.get(1)

        if count_5 is None and count_1 is None:
            logger.info("Paper {} has no citations".format(query))
            citations_filtered.pop(query)
            master_counter.update({"all_missing"})
            continue

        if count_5 is None:
            logger.info("Paper {} has no direct citations".format(query))
            master_counter.update({"count_5_missing"})
        if count_1 is None:
            logger.info("Paper {} has no hard negative citations".format(query))
            master_counter.update({"count_1_missing"})


    output_path = "final_citation_data_filtered.json"
    save(output_path, citations_filtered)

    missing_data_output_path = "missing_citation_data.json"
    save(missing_data_output_path, master_counter)

def save(output_path, output):
    logger.info("Saving to path {}".format(output_path))
    with open(output_path, "w") as f:
        f.write(json.dumps(output))
    logger.info("Saved.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--citations", default="final_citation_data.json")
    args = ap.parse_args()
    citations = args.citations

    main(citations)