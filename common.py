import logging

logging.basicConfig(filename='micro-signal.log', level=logging.INFO)


def log_info(message):
    logging.info(message)
    print(message)


def log_error(message):
    logging.error(message)
    print(message)