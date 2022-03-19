from loguru import logger

from tasks.celery import app


__all__ = ["add"]


@app.task
def add(x, y):
    logger.debug(f"User request adding <{x}> to <{y}>.")

    result = x + y

    logger.debug(f"Task solve request with result <{result}>.")

    return result


@app.task
def sub(x, y):
    logger.debug(f"User request subtract <{y}> from <{x}>.")

    result = x - y

    logger.debug(f"Task solve request with result <{result}>.")

    return result


@app.task
def mul(x, y):
    logger.debug(f"User request multiply <{x}> by <{y}>.")

    result = x * y

    logger.debug(f"Task solve request with result <{result}>.")

    return result


@app.task
def divide(x, y):
    logger.debug(f"User request divide <{x}> into <{y}>.")

    result = x * y

    logger.debug(f"Task solve request with result <{result}>.")

    return result
