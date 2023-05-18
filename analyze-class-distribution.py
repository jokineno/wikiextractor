import argparse
import json 
from common import setup_logging

logger = setup_logging()

def main(metadata_path):
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    with open("id2title.json", "r") as f:
        id2titlemap = json.load(f)

    cross_link_distribution = {}
    for paper_id, data in metadata.items():
        for cls_id in data['classes']:
            if cls_id in cross_link_distribution:
                cross_link_distribution[cls_id]['count'] += 1
            else:
                class_name = id2titlemap.get(cls_id)
                cross_link_distribution[cls_id] = {"count": 1, "class_name": class_name}
    

    sorted_cross_link_distribution = sorted(cross_link_distribution.items(), key=lambda x: x[1]['count'])
    sorted_cross_link_distribution = dict(sorted_cross_link_distribution)

    output_path = "wiki_link_distributions.json"
    logger.info("Saving data to {}".format(output_path))
    with open(output_path, "w") as f:
        f.write(json.dumps(sorted_cross_link_distribution))
    logger.info("Saved.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", default="metadata.json")
    args = ap.parse_args()
    metadata_path = args.metadata 
    main(metadata_path)