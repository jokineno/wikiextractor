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

from common import setup_logging
import sys
log_file = sys.argv[0] + ".log"
logger = setup_logging(log_output=log_file)


cache = {}

count = 0
not_found = set()

def get_metadata_articles():
    with open("metadata.json", "r") as f:
        data = json.load(f)
    return data 

def get_hard_negatives(P1, P2_list, data, valid_articles, debug):
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
        
        
        if debug:
            if "1024" in P3_list:
                print("FOUND")
                print(f"citation: {P2}, citations: {P3_list}")
                print(f"hard_negatives: {hard_negatives}")
        # Basically all citations of a paper cited by the query paper are hard negatives.  
        hard_negatives.update(P3_list)
        # Just remove those that are also cited by the query paper. So P1 !=> P3 works. 
        hard_negatives = hard_negatives.difference(P2_list)

        if debug and "1024" in P3_list:
            print(f"hard_negatives after updated: {hard_negatives}")
            print(f"hard_negative after filtering: {hard_negatives}")
            print("-----------\n\n")
        
        #if debug:
        #    print(f"HN: {P2}: {hard_negatives}\n")
        all_hard_negatives.update(list(hard_negatives))

    all_hard_negatives = list(all_hard_negatives)
    final = []
    for article in all_hard_negatives:
        if valid_articles.get(article) is None:
            continue
        final.append(article) 


    if debug:
        print(f"Query: {P1}, Citations:{P2_list}, All Hard Negatives: {final}")


    if any(HN in P2_list for HN in final):
        raise Exception(f"HARD NEGATIVE CANNOT BE CITED BY THE QUERY PAPER. Query Paper {P1} ")

    return final


x = 0
hard_mapping = {}
prev_size = 0
debug = False
print(sys.argv)
if "--debug" in sys.argv:
    debug = True

debug_id = None
if debug:
    debug_id = sys.argv[2]
    print(f"Debug mode. debug_id: {debug_id}")



with open("direct_citations.json", "r") as f:
    data = json.load(f)


valid_articles = get_metadata_articles()
for query_paper_id, citations in tqdm(data.items()):
    if debug is True and query_paper_id != debug_id:
        continue       
    if x % 50_000 == 0:
        print(f"Handling {x}/{len(data)}")
    query_references = list(citations.keys())
    hard_negatives = get_hard_negatives(query_paper_id, query_references, data, valid_articles, debug)
    hard_mapping[query_paper_id] = {article_id: {"count": 1} for article_id in hard_negatives}
    file_size = sys.getsizeof(hard_mapping) / 1000 / 1000
    file_size_100 = round(file_size / 100) * 100

    if file_size_100 % 100 == 0 and file_size_100 > prev_size:
        prev_size = file_size_100
        print(f"File size {file_size}")
    
    x+=1

output_path = "hard_negatives.json"
errors_path = "not_found_errors.json"
with open(output_path, "w") as f:
    f.write(json.dumps(hard_mapping))

with open(errors_path, "w") as f:
    f.write(json.dumps(list(not_found)))
