import logging

def setup_logging(log_output):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_output),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()