from loguru import logger


__all__ = ["add", "sub", "mul", "divide", "xsum"]


def add(x, y):
    logger.debug(f"Call `add` function with args <{x, y}>.")
    result = x + y
    logger.debug(f"Calculations result is <{result}>.")
    return result


def sub(x, y):
    logger.debug(f"Call `sub` function with args <{x, y}>.")
    result = x - y
    logger.debug(f"Calculations result is <{result}>.")
    return result


def mul(x, y):
    logger.debug(f"Call `mul` function with args <{x, y}>.")
    result = x * y
    logger.debug(f"Calculations result is <{result}>.")
    return result


def divide(x, y):
    logger.debug(f"Call `divide` function with args <{x, y}>.")
    result = x / y
    logger.debug(f"Calculations result is <{result}>.")
    return result


def xsum(numbers):
    logger.debug(f"Call `xsum` function with args <{numbers}>.")
    result = sum(numbers)
    logger.debug(f"Calculations result is <{result}>.")
    return result
