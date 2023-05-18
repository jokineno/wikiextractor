import argparse
import json
import random
from common import setup_logging
logger = setup_logging()


def filter_dict_by_keylist(d, l):
    """
    Keep only keys in d that contain in list l
    """
    return dict(filter(lambda val: val[0] in l, d.items()))


def main(metadata, citations, is_test, sample_size):
    # load the data
    logger.info("Reading metadata from path '{}'".format(metadata))
    with open(metadata, 'r') as f:
        data = json.load(f)

    logger.info("Reading citation graph from path '{}'".format(citations))
    with open(citations, 'r') as f:
        citation_graph = json.load(f)

    logger.info("Metadata lenght: {}".format(len(data)))
    logger.info("Citation graph paper count: {}".format(len(citation_graph)))

    # select papers with at least 5 references
    logger.info("Incude papers having 5 or more references (wiki cross links) ")
    # paper has at least 5 references and is part of valid papers
    papers = [paper for paper in data.values() if len(paper.get('references', [])) >= 5 and paper['paper_id'] in citation_graph]
    logger.info("Papers length after filtering {}".format(len(papers)))
    # select 1000 papers at random
    logger.info("Sample {} random papers".format(sample_size))
    query_papers = random.sample(papers, sample_size)

    output = {}
    for paper in query_papers:
        output[paper['paper_id']] = {'cited': [], 'uncited': []}
        references = paper['references']
        selected_cited_papers = random.sample(references, 5)
        for p in selected_cited_papers:
            output[paper['paper_id']]['cited'].append(p)
        for i in range(25):
            # select a random paper that is not in the reference list
            while True:
                random_paper = random.choice(papers)
                if random_paper['paper_id'] not in references:
                    break
            output[paper['paper_id']]['uncited'].append(random_paper['paper_id'])

    # write the results to a .qrel file
    if is_test:
        name = "test.qrel"
    else:
        name = "val.qrel"
    output_path = "./holdout/scidocs_citation_data/{}".format(name)
    logger.info("Writing output to {}".format(output_path))
    with open(output_path, 'w') as f:
        for paper_id, items in output.items():
            for reference in items['cited']:
                f.write(f"{paper_id} 0 {reference} 1\n")
            for other_paper in items['uncited']:
                f.write(f"{paper_id} 0 {other_paper} 0\n")

    sample_ids = set()
    # add all the query papers
    for paper, items in output.items():
        sample_ids.add(paper)
        for cited_paper in items['cited']:
            sample_ids.add(cited_paper)
        for uncited_paper in items['uncited']:
            sample_ids.add(uncited_paper)

    output_path = "./holdout/citation/{}".format("sample.ids")
    logger.info("Writing output to {}".format(output_path))
    with open(output_path, "w") as f:
        for paper_id in sample_ids:
            f.write(f"{paper_id}\n")

    output_path = "./holdout/citation/{}".format("sample-metadata.json")
    logger.info("Writing output to {}".format(output_path))
    sample_metadata = filter_dict_by_keylist(data, list(sample_ids))
    with open(output_path, "w") as f:
        f.write(json.dumps(sample_metadata))
    logger.info("Done")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", default="metadata.json")
    ap.add_argument("--citations", default="./holdout/data.json")
    ap.add_argument("--is_test_val", choices=['test','val'], help="Specify test or val")
    ap.add_argument("--sample_size", default=1000, type=int)
    args = ap.parse_args()

    if args.is_test_val == "test":
        is_test = True
    elif args.is_test_val == "val":
        is_test = False
    else:
        raise Exception("Invalid 'is_test_val' argument.")

    main(metadata=args.metadata, citations=args.citations, is_test=is_test, sample_size=args.sample_size)