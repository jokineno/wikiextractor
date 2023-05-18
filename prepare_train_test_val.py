import os.path

import json
from sklearn.model_selection import train_test_split
import argparse
import random

from common import setup_logging
import sys
log_file = sys.argv[0] + ".log"
logger = setup_logging(log_output=log_file)
random.seed(10)


class Writer():
    def __init__(self, output_path):
        self.output_path = output_path
        self.out = open(output_path, "w")

    def write(self, data):
        line = data + "\n"
        self.out.write(line)

    def close(self):
        self.out.close()
        logger.info(f"Finished writing {self.output_path}")


def main(sample_size, output_path, training_dir, holdout_dir, metadata_path, citations_path):

    with open(metadata_path, "r") as f:
        data = json.load(f)

    with open(citations_path, "r") as f:
        citations = json.load(f)

    # Split citations to train and holdout sets
    total_count = len(citations.keys())
    holdout_set_size = int(total_count * 0.2)  # round to integer
    citation_key_list = list(citations.keys())

    holdout_citation_keys = random.sample(citation_key_list, holdout_set_size)
    holdout_citations = {}
    for key in holdout_citation_keys:
        holdout_citations[key] = citations.pop(key)

    training_set_size = len(list(citations.keys()))

    holdout_output_path = "{}/data.json".format(holdout_dir)
    logger.info("Total citations count {}, Training count: {},  Holdout count {}.".format(total_count, training_set_size, holdout_set_size))
    with open(holdout_output_path, "w") as f:
        f.write(json.dumps(holdout_citations))
        logger.info("Saved holdout citations to {}".format(holdout_output_path))

    training_output_path = "{}/data.json".format(training_dir)
    with open(training_output_path, "w") as f:
        f.write(json.dumps(citations))
        logger.info("Saved training citations to {}".format(holdout_output_path))


    articles = list(citations.keys())

    if sample_size is not None and isinstance(sample_size, int):
        logger.info("Generating {} samples".format(sample_size))
        articles = random.sample(articles, sample_size)

    total = len(articles)
    logger.info("Total articles: {}".format(total))

    train_and_val, test = train_test_split(articles, test_size=0.2, random_state=1)

    # 0.8x * y = 0.1x
    # 0.1x / 0.8x = y

    train, val = train_test_split(train_and_val, test_size=0.125, random_state=1)

    test_fraq = len(test) / total
    val_fraq = len(val) / total
    train_fraq = len(train) / total

    logger.info(f"train size: {len(train)} ({train_fraq}),\ntest_size = {len(test)} ({test_fraq}),\n validation size = {len(val)} ({val_fraq})")

    for name, dataset in zip(["train.txt", "test.txt", "val.txt"], [train, test, val]):

        path = output_path.strip("/") + "/" + name
        logger.info("Writing file {} to {}".format(name, path))
        writer = Writer(path)
        for sample_id in dataset:
            writer.write(sample_id)

        writer.close()
    all_keys_output_path = output_path.strip("/") + "/" + "all.txt"
    logger.info("Saving all keys to {}".format(all_keys_output_path))
    with open(all_keys_output_path, "w") as f:
        f.write(json.dumps(articles))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample_size", type=int, help="sample x articles from all data.")
    parser.add_argument("--output_path", default="training")
    parser.add_argument("--holdout_dir", default="holdout")
    parser.add_argument("--training_dir", default="training")
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--citations", required=True)

    args = parser.parse_args()
    sample_size = args.sample_size
    output_path = args.output_path
    holdout_dir = args.holdout_dir
    training_dir = args.training_dir
    metadata_path = args.metadata
    citations_path = args.citations

    main(sample_size, output_path, training_dir, holdout_dir, metadata_path, citations_path)
