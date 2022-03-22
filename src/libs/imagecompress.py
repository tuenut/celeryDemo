from random import randint
from time import sleep

from loguru import logger


def check_file(path_to_file: str) -> bool:
    """Check that file exists."""

    sleep(1)
    return randint(0, 100) > 50


def compress(path_to_file: str) -> bool:
    """Apply the best compression algorithm."""

    logger.debug("Start compression...")

    progress = 0
    while progress < 100:
        _add = randint(3, 20)
        if _add + progress > 100:
            _add = 100 - progress

        progress += _add
        logger.debug(f"Status of compressing: {progress}%")

        sleep(randint(10, 100)/100)

    logger.debug("Compressing complete.")

    return True


def compress_jpeg(path_to_file: str):
    logger.debug("Checking file extension.")
    if not (path_to_file.endswith(".jpg") or path_to_file.endswith(".jpeg")):
        raise TypeError("Wrong file type.")
    logger.debug("Ok.")

    logger.debug("Checking file existence.")
    if not check_file(path_to_file):
        raise FileNotFoundError("User file not found.")
    logger.debug("Ok.")

    compress(path_to_file)
