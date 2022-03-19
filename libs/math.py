from loguru import logger


def add(x, y):
    logger.debug(f"Call `add` function with args <{x, y}>.")
    result = x + y
    logger.debug(f"Calculations result is <{result}>.")
    return result


def sub(x, y):
    logger.debug(f"Call `add` function with args <{x, y}>.")
    result = x - y
    logger.debug(f"Calculations result is <{result}>.")
    return result


def mul(x, y):
    logger.debug(f"Call `add` function with args <{x, y}>.")
    result = x * y
    logger.debug(f"Calculations result is <{result}>.")
    return result


def divide(x, y):
    logger.debug(f"Call `add` function with args <{x, y}>.")
    result = x / y
    logger.debug(f"Calculations result is <{result}>.")
    return result
