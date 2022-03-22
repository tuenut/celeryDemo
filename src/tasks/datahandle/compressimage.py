from loguru import logger

from libs.imagecompress import compress_jpeg
from tasks.celery import app


__all__ = ["compress_image"]


@app.task
def compress_image(path_to_file: str):
    logger.info(f"Run compress image task for file <{path_to_file}>.")

    try:
        compress_jpeg(path_to_file)
    except:
        logger.exception("Something goes wrong.")
        raise
    else:
        logger.info(f"File <{path_to_file}> compressed.")
