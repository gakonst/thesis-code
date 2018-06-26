import logging
import sys
import os

def configure_logging(_id):
    # Configure logging
    logger = logging.getLogger("Meter "+_id)
    formatter = logging.Formatter('%(asctime)s %(levelname)s | {} %(message)s'.format(_id))
    hdlr = logging.StreamHandler(sys.stdout)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    if 'DEBUG' in os.environ:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger
