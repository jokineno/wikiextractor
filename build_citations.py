import glob
import json 
from tqdm import tqdm


def get_files():
    wiki_files = glob.glob("./text/*/wiki*")
    return wiki_files 

def get_metadata():
    with open("metadata.json", "r") as f:
        data = json.load(f)
    return data 

output = {}

'''
Some of the articles are empty. 
metadata.json should contain only non empty articles 
=> if cited article exists an has text => keep it, other wise dump it.
'''
valid_articles = get_metadata()
skip_cache = {}
cited_articles_not_in_metadata = []
wiki_files = get_files()
for wiki in tqdm(wiki_files):
    with open(wiki, "r") as f:
        data = f.read()
    
    for sample in data.splitlines():
        sample = json.loads(sample)
        sample_id = sample["id"]
        if valid_articles.get(sample_id) is None:
            continue
        reference_list = sample["introduction_references"]
        if len(reference_list) > 0:
            reference_list = reference_list[0]
            direct_citations = []
            for item in reference_list:
                article_id = item["article_id"]
                if article_id == "##NOT_FOUND##":
                    continue
                """
                Do not add articles that does not exist in metadata.json 
                """
                if valid_articles.get(article_id) is None:
                    cited_articles_not_in_metadata.append(article_id)
                    continue

                direct_citations.append(article_id)

            output[sample_id] = {article_id: {"count":5} for article_id in direct_citations}
        else:
            output[sample_id] = {}    

output_path = "direct_citations.json"
with open(output_path, "w") as f:
    f.write(json.dumps(output))

with open("directly_cited_articles_not_in_metadata.json", "w") as f:
    f.write(json.dumps(cited_articles_not_in_metadata))
