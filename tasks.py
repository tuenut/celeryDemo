from celery import Celery
from loguru import logger


app = Celery(
    'tasks',  # entry point module name
    broker='redis://localhost',  # where celery send tasks, and where workers get it
    backend='redis://localhost'  # where task results should store
)


@app.task
def add(x, y):
    logger.debug(f"Call task with args <{(x, y)}>.")

    result = x + y

    logger.debug(f"Task solve request with result <{result}>.")

    return x + y
