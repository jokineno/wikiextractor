import sys

import json
import argparse
"""
This script reads metadata.json and final_citation_data.json and checks if there are problems. 
"""

from common import setup_logging
import sys
log_file = sys.argv[0] + ".log"
logger = setup_logging(log_output=log_file)

def extract_articles(citations):
    """
    Citations is a dict object containing
    "query_paper_key": {
        "cited_paper_key": {"count": 1 } : here 1 represents hard negative.
    }
    """
    logger.info("Starting to extract articles ids...")
    articles = set()
    try:
        for article_id, other_papers in citations.items():
            articles.add(article_id) # add the article
            articles.update(list(other_papers.keys())) # add all the referenced articles and
    except AttributeError:
        print(citations)
        raise Exception("error")

    logger.info("Done extracting..")
    return articles

def main(metadata_path, citations_path):
    # open metadata
    logger.info("Reading metadata from {}".format(metadata_path))
    with open(metadata_path, "r") as f:
        metadatas = json.load(f)

    # open final citation data
    logger.info("Reading {}".format(citations_path))
    with open(citations_path, "r") as f:
        citations = json.load(f)

    all_articles = extract_articles(citations)

    valid = []
    invalid = []
    other = []
    try:
        for article in all_articles:
            metadata = metadatas.get(article)
            if metadata is None:
                invalid.append(article)
                # print(f"invalid article: {article}")
                continue
            if type(metadata) is dict:
                valid.append(article)
            else:
                other.append(article)
                raise Exception(f"This should not happen. {article}")

    except Exception as e:
        raise Exception(e)

    print(f"Count of valid articles: {len(valid)}")
    print(f"Count of invalid articles: {len(invalid)}")
    print(f"Count of other articles: {len(other)}")

    if len(invalid) > 5:
        print("======5 FIRST INVALID ARTICLES======")
        for n, i in enumerate(invalid[:5]):
            print(f"{n + 1}. example: (id={i}) {metadatas.get(i)}")

        print("\n\n")
        print("======5 FIRST VALID ARTICLES======")
        for n, i in enumerate(valid[:5]):
            print(f"{n + 1}. example: (id={i}) {metadatas.get(i)}")

    if len(invalid) == 0 and len(other) == 0 and len(valid) > 0:
        print("All articles have existing metadata! Move on to training.")




if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--citations", default="final_citation_data_filtered.json")
    ap.add_argument("--metadata", default="metadata.json")
    args = ap.parse_args()
    citations_path = args.citations
    metadata_path = args.metadata
    main(metadata_path, citations_path)