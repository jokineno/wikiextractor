import argparse
import json 
from common import setup_logging

logger = setup_logging()

def handle_metadata(metadata):
    pass


def add(data, cid, id2title):
    """
    Data: citation data
    cid: class id
    id2title: id to title map
    """
    if cid in data:
        data[cid]['count'] += 1
    else:
        class_name = id2title.get(cid)
        data[cid] = {'count': 1, "class_name": class_name}


def handle_citation(citations, metadata, id2title):
    logger.info("[*] Starting to create link count distribution per class.")
    class_dist = {}
    for paper_id, data in citations.items():
        paper_data = metadata[paper_id]
        for cls_id in paper_data['classes']:
            add(class_dist, cls_id, id2title)
    return class_dist


def main(metadata_path, citation_path):
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    with open(citation_path, "r") as f:
        citation = json.load(f)

    with open("id2title.json", "r") as f:
        id2titlemap = json.load(f)

    cross_link_distribution = {}
    for paper_id, data in metadata.items():
        for cls_id in data['classes']:
            add(cross_link_distribution, cls_id, id2titlemap)

    sorted_cross_link_distribution = sorted(cross_link_distribution.items(), key=lambda x: x[1]['count'])
    sorted_cross_link_distribution = dict(sorted_cross_link_distribution)

    output_path = "./holdout/wiki_class_distributions_metadata.json"
    logger.info("[*] Saving data to {}".format(output_path))
    with open(output_path, "w") as f:
        f.write(json.dumps(sorted_cross_link_distribution))
    logger.info("[*] Saved.")

    class_dist = handle_citation(citation, metadata, id2titlemap)
    sorted_class_dist = dict((sorted(class_dist.items(), key=lambda x: x[1]['count'])))
    output_path = "./holdout/wiki_class_distributions_data.json"
    logger.info("[*] Saving data to {}".format(output_path))
    with open(output_path, "w") as f:
        f.write(json.dumps(sorted_class_dist))
    logger.info("[*] Saved.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", default="metadata.json", help="Path to metadata file")
    ap.add_argument("--citation", default="./holdout/data.json", help="Path citations data file.")
    args = ap.parse_args()
    metadata_path = args.metadata 
    citation_path = args.citation
    main(metadata_path, citation_path)