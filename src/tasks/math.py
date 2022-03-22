from loguru import logger

from tasks.celery import app
from libs.math import add, sub, mul, divide, xsum


__all__ = [
    "add_request", "sub_request", "mul_request", "divide_request",
    "xsum_request"
]


@app.task
def add_request(x, y):
    logger.info(f"User request adding <{x}> to <{y}>.")

    result = add(x, y)

    logger.info(f"Task solve request with result <{result}>.")

    return result


@app.task
def sub_request(x, y):
    logger.info(f"User request subtract <{y}> from <{x}>.")

    result = sub(x, y)

    logger.info(f"Task solve request with result <{result}>.")

    return result


@app.task
def mul_request(x, y):
    logger.info(f"User request multiply <{x}> by <{y}>.")

    result = mul(x, y)

    logger.info(f"Task solve request with result <{result}>.")

    return result


@app.task
def divide_request(x, y):
    logger.info(f"User request divide <{x}> into <{y}>.")

    result = divide(x, y)

    logger.info(f"Task solve request with result <{result}>.")

    return result


@app.task
def xsum_request(numbers):
    logger.info(f"User request summarize <{numbers}>.")

    result = xsum(numbers)

    logger.info(f"Task solve request with result <{result}>.")

    return result


