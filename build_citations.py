import glob
import json 
from tqdm import tqdm

from common import setup_logging
import sys
log_file = sys.argv[0] + ".log"
logger = setup_logging(log_output=log_file)


def get_metadata():
    with open("metadata.json", "r") as f:
        data = json.load(f)
    return data 

output = {}

def main():

    '''
    Some of the articles are empty.
    metadata.json should contain only non empty articles
    => if cited article exists an has text => keep it, other wise dump it.
    '''
    metadata = get_metadata()
    articles_without_links = []
    not_found_in_metadata = []
    for key, data in metadata.items():
        paper_id = data['paper_id']

        if key != paper_id: #THIS SHOULD NOT HAPPEN
            raise Exception("key does not equal to paper id")

        direct_wiki_links = data['references']
        if type(direct_wiki_links) is not list:
            raise Exception("data['references'] is not list type")

        if len(direct_wiki_links) == 0:
            articles_without_links.append(paper_id)

        citations = {}
        for linked_article_id in list(direct_wiki_links):
            if metadata.get(linked_article_id):
                citations.update(
                    {
                        linked_article_id: {'count': 5}
                     }
                )
            else:
                not_found_in_metadata.append(linked_article_id)

        output[paper_id] = citations

    print("========Articles without links count: {}========".format(len(articles_without_links)))
    print("========Articles not found in metadata: {}========".format(len(not_found_in_metadata)))


    save("direct_citations.json", output)
    save("articles_without_links.json", articles_without_links)
    save("articles_not_found_in_metadata.json", not_found_in_metadata)


def save(output_path, output):
    logger.info("Saving to path {}".format(output_path))
    with open(output_path, "w") as f:
        f.write(json.dumps(output))
    logger.info("Saved.")


if __name__ == "__main__":
    main()