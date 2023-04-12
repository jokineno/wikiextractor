import json 
"""
This script reads metadata.json and final_citation_data.json and checks if there are problems. 
"""


# open metadata 
with open("metadata.json", "r") as f:
    metadatas = json.load(f)

# open final citation data 
with open("final_citation_data.json", "r") as f:
    citations = json.load(f)

def extract_articles(citations):
    articles = set()
    for article_id, other_papers in citations.items():
        articles.add(article_id)
        articles.update(list(other_papers.keys()))
    return articles

all_articles = extract_articles(citations)

valid = []
invalid = []
other = []
for article in all_articles:
    metadata = metadatas.get(article)
    if metadata is None:
        invalid.append(article)
        #print(f"invalid article: {article}")
        continue
    if type(metadata) is dict:
        valid.append(article)
    else:
        other.append(article)
        raise Exception(f"This should not happen. {article}")


print(f"Count of valid articles: {len(valid)}")
print(f"Count of invalid articles: {len(invalid)}")
print(f"Count of other articles: {len(other)}")

if len(invalid) > 5:
    for n, i in enumerate(invalid[:5]):
        print(f"{n+1}. example: (id={i}) {metadatas.get(i)}")

    for n,i in enumerate(valid[:5]):
        print(f"{n+1}. example: (id={i}) {metadatas.get(i)}")


if len(invalid) == 0 and len(other) == 0 and len(valid) > 0:
    print("All articles have existing metadata! Move on to training.")  