import argparse
import json 
from common import setup_logging

logger = setup_logging()

def handle_metadata(metadata):
    pass

def add(data, cid, id2title):
    if cid in data:
        data[cid]['count'] += 1
    else:
        class_name = id2title.get(cid)
        data[cid] = {'count': 1, "class_name": class_name}
    return data


def handle_citation(citations, metadata, id2title):
    logger.info("Starting to handle citations.")
    class_dist = {}
    for paper_id, data in citations.items():
        paper_data = metadata[paper_id]
        for cls_id in paper_data['classes']:
            class_dist = add(class_dist, cls_id, id2title)
    logger.info("Finished handling citations.")

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
            cross_link_distribution = add(cross_link_distribution, cls_id, id2titlemap)

    sorted_cross_link_distribution = sorted(cross_link_distribution.items(), key=lambda x: x[1]['count'])
    sorted_cross_link_distribution = dict(sorted_cross_link_distribution)

    output_path = "./holdout/wiki_class_distributions_metadata.json"
    logger.info("Saving data to {}".format(output_path))
    with open(output_path, "w") as f:
        f.write(json.dumps(sorted_cross_link_distribution))
    logger.info("Saved.")

    class_dist = handle_citation(citation, metadata, id2titlemap)
    sorted_class_dist = dict((sorted(class_dist.items(), key=lambda x: x[1]['count'])))
    output_path = "./holdout/wiki_class_distributions_data.json"
    logger.info("Saving data to {}".format(output_path))
    with open(output_path, "w") as f:
        f.write(json.dumps(sorted_class_dist))
    logger.info("Saved.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", default="metadata.json")
    ap.add_argument("--citation", default="./holdout/data.json")
    args = ap.parse_args()
    metadata_path = args.metadata 
    citation_path = args.citation
    main(metadata_path, citation_path)