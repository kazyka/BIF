import logging
import os

LOGLEVEL = os.environ.get("BIF_LOGLEVEL", "INFO")

log_format = "[%(asctime)s] - %(relativeCreated)-8d %(name)-30s %(levelname)-8s %(message)s"

fh = logging.FileHandler('bif.log')
fh.setLevel(LOGLEVEL)
fh.setFormatter(logging.Formatter(log_format,datefmt='%a, %d %b %Y %H:%M:%S'))

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(log_format))


logger = logging.getLogger("bif")
logger.setLevel(LOGLEVEL)
logger.addHandler(handler)
logger.addHandler(fh)


def log_level(level):
    if level == "DISABLE":
        logging.disable(level=logging.CRITICAL)
    else:
        logger.setLevel(level)
