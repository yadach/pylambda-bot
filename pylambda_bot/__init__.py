import logging
import sys


def init_logging(log_level: str = "DEBUG"):
    """Initialize logging.

    Args:
        log_level (str, optional): Log level. Defaults to "DEBUG".
    """
    logger = logging.getLogger("pylambda_bot")
    logger.propagate = False
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("[%(levelname)s] (%(module)s:%(funcName)s:%(lineno)d): %(message)s")
    )
    handler.setLevel(log_level)
    logger.setLevel(log_level)
    logger.addHandler(handler)


init_logging()
