import logging


def log_info(message, print_text=False):
    logging.basicConfig(filename='micro-signal-info.log', level=logging.INFO)
    logging.info(message)
    if print_text:
        print(message)


def log_error(message, print_text=False):
    logging.basicConfig(filename='micro-signal-error.log', level=logging.ERROR)
    logging.error(message)
    if print_text:
        print(message)
