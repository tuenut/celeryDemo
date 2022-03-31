from random import choice, randint

from loguru import logger

from libs.requests import request


def _connect_to_weather_provider(timeout: int = 5):
    logger.debug(f"Connecting to weateher provider...")

    request(timeout)

    logger.debug("Connection established.")

    return True


def _get_data(connection, timeout: int = 5):
    if not connection:
        raise Exception("Can not connect to provider.")

    logger.debug("Getting data...")

    request(timeout)

    data = {
        "weather": choice(["clean", "rain", "storm", "cloudy", "snow"]),
        "temperature": randint(0, 17) - 10
    }
    logger.debug("Data received.")

    return data


def get_weather(day: str = "today", timeout: int = 5) -> dict:
    logger.debug(f"Start getting weather for <{day}>.")

    connection = _connect_to_weather_provider(timeout)
    data = _get_data(connection)

    return data
