from common import setup_logging
import sys 
import argparse
import json
log_file = sys.argv[0] + ".log"
logger = setup_logging(log_file)


def read_file(filepath):
    logger.info("[*] Reading file {}".format(filepath))
    with open(filepath, "r") as f:
        data = json.load(f)
    return data


def filter_dict_by_keylist(d, l):
    """
    Keep only keys in d that contain in list l
    """
    return dict(filter(lambda val: val[0] in l, d.items()))


def main(metadata_path, citations_path, idlist_path, output_dir):
    metadata = read_file(metadata_path)
    citations = read_file(citations_path)
    idlist = read_file(idlist_path)
    metadata_filtered = filter_dict_by_keylist(metadata, idlist)
    citations_filtered = filter_dict_by_keylist(citations, idlist)

    # check lenghts
    logger.info("[*] 'idlist' length {}".format(len(idlist)))
    logger.info("[*] 'filtered' metadata length {}".format(len(metadata_filtered)))
    logger.info("[*] 'filtered' citations length {}".format(len(citations_filtered)))

    for name, dataset in zip(["metadata.json", "data.json"], [metadata_filtered, citations_filtered]):
        output_path = output_dir.strip("/") + "/" + name
        logger.info("[*] Saving file to path {}".format(output_path))
        with open(output_path, "w") as f:
            f.write(json.dumps(dataset))
        logger.info("[*] Saved file {}".format(output_path))


if __name__ == "__main__":
    logger.info("[*] Start.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--citations", required=True)
    parser.add_argument("--idlist", required=True)
    parser.add_argument("--output_dir", required=True)

    args = parser.parse_args()
    metadata = args.metadata
    citations = args.citations
    paper_id_list = args.idlist
    output_dir = args.output_dir

    main(metadata, citations, paper_id_list, output_dir)
    logger.info("[*] Finished.")