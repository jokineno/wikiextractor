from common import setup_logging, Writer
import sys 
import argparse
import json
from random import sample
log_file = sys.argv[0] + ".log"
logger = setup_logging(log_file)


def read_file(filepath):
    logger.info("Reading file {}".format(filepath))
    with open(filepath, "r") as f:
        data = json.load(f)
    return data

def filter_dict_by_keylist(d, l):
    """
    Keep only keys in d that contain in list l
    """
    return dict(filter(lambda val: val[0] in l, d.items()))


def main(metadata_path, citations_path, sample_size, output_dir):
    citations = read_file(citations_path)
    metadata = read_file(metadata_path)

    all_keys = list(citations.keys())
    sample_ids_for_embedding = sample(all_keys, sample_size)
    sample_metadata = filter_dict_by_keylist(metadata, sample_ids_for_embedding)

    # check lenghts
    logger.info("sample_ids_for_embedding length {}".format(len(sample_ids_for_embedding)))
    logger.info("sample_metadata length {}".format(len(sample_metadata)))
    for name, dataset in zip(["sample-metadata.json"], [sample_metadata]):
        output_path = output_dir.strip("/") + "/" + name
        logger.info("Saving file to path {}".format(output_path))
        with open(output_path, "w") as f:
            f.write(json.dumps(dataset))
        logger.info("Saved file {}".format(output_path))

    output_path = output_dir.strip("/") + "/" + "sample.ids"
    logger.info("Saving file to path {}".format(output_path))
    row_writer = Writer(output_path)
    for i in sample_ids_for_embedding:
        row_writer.write(i)
    logger.info("Done writing")

if __name__ == "__main__":
    logger.info("Start.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--citations", required=True, help="Citation data from hold out set")
    parser.add_argument("--metadata", required=True, help="Citation data from hold out set")
    parser.add_argument("--sample_size", required=True, type=int)
    parser.add_argument("--output_dir", required=True)

    args = parser.parse_args()
    citations = args.citations
    metadata = args.metadata
    sample_size = args.sample_size
    output_dir = args.output_dir

    main(metadata, citations, sample_size, output_dir)
    logger.info("Finished.")