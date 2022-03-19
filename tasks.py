from celery import Celery
from loguru import logger


app = Celery("tasks")
app.config_from_object("celeryconfig")


@app.task
def add(x, y):
    logger.debug(f"Call task with args <{(x, y)}>.")

    result = x + y

    logger.debug(f"Task solve request with result <{result}>.")

    return x + y
