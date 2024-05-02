import logging

def setup_logging(log_output=None):
    if log_output is None:
        handlers = [
            logging.StreamHandler()
        ]
    else:
        handlers = [
            logging.FileHandler(log_output),
            logging.StreamHandler()
        ]

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )
    return logging.getLogger()


logger = setup_logging()


class Writer():
    def __init__(self, output_path):
        self.output_path = output_path
        self.out = open(output_path, "w")

    def write(self, data):
        line = data + "\n"
        self.out.write(line)

    def close(self):
        self.out.close()
        logger.info(f"Finished writing {self.output_path}")

def read_json(file_path):
    import json
    print("[*] Reading json file: {}".format(file_path))
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

def make_dirs(output_dir):
    import os
    if not os.path.exists(output_dir):
        logger.info("[*] Creating output_dir {}".format(output_dir))
        os.makedirs(output_dir)



def filter_dict_by_keylist(d, l):
    """
    Keep only keys in d that contain in list l
    """
    return dict(filter(lambda val: val[0] in l, d.items()))


def article_exists(metadata: dict, article_id: str) -> bool:
    data = metadata.get(article_id, {})
    title = data.get('title', None)
    abstract = data.get('abstract', None)
    return title and abstract