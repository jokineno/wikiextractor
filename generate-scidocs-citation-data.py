import argparse
import copy
import time
import json
import random
import sys

from common import setup_logging
logger = setup_logging()
random.seed(1)


def filter_dict_by_keylist(d, l):
    """
    Keep only keys in d that contain in list l
    """
    return dict(filter(lambda val: val[0] in l, d.items()))

def filter_dictionary(dictionary, selected_keys):
    now = time.time()
    filtered_dict = {}
    total_count = len(dictionary)
    for i, (key, value) in enumerate(dictionary.items()):
        if i % 10000 == 0:
            logger.info("{}/{}".format(i, total_count))
        if key in selected_keys:
            filtered_dict[key] = value

    print("Took {} seconds".format(time.time() -now))
    return filtered_dict

def filter_dictionary_2(dictionary, selected_keys):
    now = time.time()
    filtered_dict = {}
    for key in selected_keys:
        filtered_dict[key] = dictionary[key]
    print("Took {} seconds".format(time.time() -now))
    return filtered_dict

def main(metadata, citations, sample_size):
    # load the data
    logger.info("Reading metadata from path '{}'".format(metadata))
    with open(metadata, 'r') as f:
        data = json.load(f)

    logger.info("Reading citation graph from path '{}'".format(citations))
    with open(citations, 'r') as f:
        citation_graph = json.load(f)

    logger.info("Metadata length: {}".format(len(data)))
    logger.info("Citation graph paper count: {}".format(len(citation_graph)))

    # select papers with at least 5 references
    logger.info("Include papers having 5 or more references (wiki cross links) ")
    # paper has at least 5 references and is part of holdout dataset
    papers = []
    for paper_id, links in citation_graph.items():
        direct_citations = [citation_id for citation_id, count in links.items() if count['count'] == 5]
        if len(direct_citations) >= 5:
            papers.append({"paper_id": paper_id, "references": direct_citations})

    logger.info("Papers length after filtering {}".format(len(papers)))
    # select 1000 papers at random
    logger.info("Sample {} random papers".format(sample_size))
    random.shuffle(papers)
    # Split the shuffled list into test and validation sets
    test_set = papers[:sample_size]  # 0 - 999
    validation_set = papers[sample_size:sample_size*2]  # 1000 - 1999

    for case, query_papers in zip(['test', 'val'], [test_set, validation_set]):
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
        if case == "test":
            name = "test.qrel"
        else:
            name = "val.qrel"

        output_path = "./holdout/citation/{}".format(name)
        logger.info("Writing output to {}".format(output_path))
        with open(output_path, 'w') as f:
            for paper_id, items in output.items():
                for reference in items['cited']:
                    f.write(f"{paper_id} 0 {reference} 1\n")
                for other_paper in items['uncited']:
                    f.write(f"{paper_id} 0 {other_paper} 0\n")
        logger.info("Done {}".format(output_path))

        sample_ids = set()
        # add all the query papers
        for paper, items in output.items():
            sample_ids.add(paper)
            for cited_paper in items['cited']:
                sample_ids.add(cited_paper)
            for uncited_paper in items['uncited']:
                sample_ids.add(uncited_paper)

        output_path = "./holdout/citation/{}".format("sample_{}.ids".format(case))
        logger.info("Writing output to {}".format(output_path))
        with open(output_path, "w") as f:
            for paper_id in sample_ids:
                f.write(f"{paper_id}\n")
        logger.info("Wrote {}".format(output_path))

        output_path = "./holdout/citation/{}".format("sample-metadata_{}.json".format(case))
        logger.info("Writing output to {}".format(output_path))
        sample_metadata = filter_dictionary_2(data, list(sample_ids))
        with open(output_path, "w") as f:
            f.write(json.dumps(sample_metadata))
        logger.info("Wrote {}".format(output_path))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", default="metadata.json")
    ap.add_argument("--citations", default="./holdout/data.json")
    ap.add_argument("--sample_size", default=1000, type=int)
    args = ap.parse_args()

    main(metadata=args.metadata, citations=args.citations, sample_size=args.sample_size)