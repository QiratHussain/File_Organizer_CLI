import logging


def setup_logger(name: str = "file-organizer") -> logging.Logger:

    logger = logging.getLogger(name)

    # Prevent duplicate handlers if called twice
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger