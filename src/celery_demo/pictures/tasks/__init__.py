from loguru import logger

from celery import shared_task

from .utils import compress_jpeg


__all__ = ["compress_image"]


@shared_task
def compress_image(path_to_file: str):
    logger.info(f"Run compress image task for file <{path_to_file}>.")

    try:
        compress_jpeg(path_to_file)
    except:
        logger.exception("Something goes wrong while task execution.")
        raise
    else:
        logger.info("Task completed")
