from loguru import logger

from celery import shared_task
from libs.logging import Logged

from .utils import add, sub, mul, divide, xsum


__all__ = [
    "add_request", "sub_request", "mul_request", "divide_request",
    "xsum_request"
]


@shared_task(bind=True)
@Logged.decorate
def add_request(self, x, y):
    logger.info(f"User request adding <{x}> to <{y}>.")

    result = add(x, y)

    logger.info(f"Task solve request with result <{result}>.")

    return result


@shared_task(bind=True)
@Logged.decorate
def sub_request(self, x, y):
    logger.info(f"User request subtract <{x}> from <{y}>.")

    result = sub(x, y)

    logger.info(f"Task solve request with result <{result}>.")

    return result


@shared_task
def mul_request(x, y):
    logger.info(f"User request multiply <{x}> by <{y}>.")

    result = mul(x, y)

    logger.info(f"Task solve request with result <{result}>.")

    return result


@shared_task
def divide_request(x, y):
    logger.info(f"User request divide <{x}> into <{y}>.")

    result = divide(x, y)

    logger.info(f"Task solve request with result <{result}>.")

    return result


@shared_task
def xsum_request(numbers):
    logger.info(f"User request summarize <{numbers}>.")

    result = xsum(numbers)

    logger.info(f"Task solve request with result <{result}>.")

    return result


