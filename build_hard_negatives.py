'''
Build hard negatives 

1. Query paper cites papers A B and C 
2. Paper A cites paper D
3. Paper D cites paper A 

=> This can be denoted as "hard negatives" since Paper D cites query paper but query paper does not cite paper D
but cites a paper that cites paper A. 

'''

import json
from tqdm import tqdm
import sys

from common import setup_logging, article_exists
import sys
log_file = sys.argv[0] + ".log"
logger = setup_logging(log_output=log_file)


cache = {}

count = 0
not_found = set()

def get_metadata():
    with open("metadata.json", "r") as f:
        data = json.load(f)
    return data 


def get_hard_negatives(P1, P2_list, data, metadata):
    #P1 = query_paper_id
    #P2_list => cross-references from query_paper
    #data = direct_citations dataset
    #valid_articles = master data => all articles
    # debug
    global not_found
    '''
    We denote as
    “hard negatives” the papers that are not cited by the
    query paper, but are cited by a paper cited by the
    query paper, i.e. if 
    P1 cite −−→ P2
    and P2 cite −−→ P3 but 
    P1 cite !!→ P3 then
    P3 is a candidate hard negative example for P
    '''
    all_hard_negatives = set()
    #citations are first level citations (cited by Query paper)
    for P2 in P2_list:
        hard_negatives = set()
        try:
            # get citations that are cited by a paper cited by the query paper
            P3_list = list(data[P2].keys())    
        except KeyError as ke:
            not_found.add(P2)
            continue
        
        
        hard_negatives.update(P3_list)
        # Just remove those that are also cited by the query paper. So full fill the P1 !=> P3 condition .
        hard_negatives = hard_negatives.difference(P2_list)
        all_hard_negatives.update(list(hard_negatives))

    all_hard_negatives = list(all_hard_negatives)
    final = []
    for article in all_hard_negatives:
        if metadata.get(article) is None: # CHECK THAT ARTICLE IS IN METADATA
            continue
        final.append(article) 

    # DOUBLE CHECK THAT HARD NEGATIVE IS NOT CITED BY THE QUERY PAPER
    if any(HN in P2_list for HN in final):
        raise Exception(f"HARD NEGATIVE CANNOT BE CITED BY THE QUERY PAPER. Query Paper {P1} ")
    return final


def main():
    x = 0
    hard_negatives_mapping = {}
    prev_size = 0
    with open("direct_citations.json", "r") as f:
        direct_citations = json.load(f)

    metadata = get_metadata()
    for query_paper_id, citations in tqdm(direct_citations.items()):
        if not article_exists(metadata, query_paper_id):
            raise Exception(f"Paper {query_paper_id} not found in metadata.")
        query_paper_links = list(citations.keys())
        try:
            hard_negatives = get_hard_negatives(query_paper_id, query_paper_links, direct_citations, metadata)
            hard_negatives_mapping[query_paper_id] = {article_id: {"count": 1} for article_id in hard_negatives}
        except TypeError as typerror:
            print("HARD NEGATIVES", hard_negatives_mapping)
            raise Exception(typerror)
        except Exception as e:
            raise Exception(e)
        file_size = sys.getsizeof(hard_negatives) / 1000 / 1000
        file_size_100 = round(file_size / 100) * 100

        if file_size_100 % 100 == 0 and file_size_100 > prev_size:
            prev_size = file_size_100
            print(f"File size {file_size}")

        x += 1

    output_path = "hard_negatives.json"
    errors_path = "not_found_errors.json"
    save(output_path, hard_negatives_mapping)
    save(errors_path, list(not_found))

def save(output_path, output):
    logger.info("Saving to path {}".format(output_path))
    with open(output_path, "w") as f:
        f.write(json.dumps(output))
    logger.info("Saved.")


if __name__ == "__main__":
    main()