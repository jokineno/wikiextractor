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
