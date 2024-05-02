import glob
import json 
from tqdm import tqdm

from common import setup_logging, article_exists
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
    articles_without_links = set()
    not_found_in_metadata = set()
    for key, data in metadata.items():
        paper_id = data['paper_id']

        if key != paper_id: #THIS SHOULD NOT HAPPEN
            raise Exception("key does not equal to paper id")

        reference_ids = data['references']
        if isinstance(reference_ids, list) is False:
            print(key, data, paper_id, reference_ids)
            raise Exception("data['references'] is not list type")

        if len(reference_ids) == 0:
            articles_without_links.add(paper_id)
            continue 

        citations = {}
        for linked_article_id in reference_ids:
            if article_exists(metadata, linked_article_id):
                citations.update(
                    {
                        linked_article_id: {'count': 5}
                     }
                )
            else:
                not_found_in_metadata.add(linked_article_id)

        output[paper_id] = citations

    print("========Output count: {}========".format(len(output)))
    print("========Articles without links count: {}========".format(len(articles_without_links)))
    print("========Articles not found in metadata: {}========".format(len(not_found_in_metadata)))


    save("direct_citations.json", output)
    save("articles_without_links.json", list(articles_without_links))
    save("articles_not_found_in_metadata.json", list(not_found_in_metadata))


def save(output_path, output):
    logger.info("Saving to path {}".format(output_path))
    with open(output_path, "w") as f:
        f.write(json.dumps(output))
    logger.info("Saved.")


if __name__ == "__main__":
    main()