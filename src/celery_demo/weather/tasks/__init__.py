from celery import shared_task
from loguru import logger

from .utils import get_weather


__all__ = ["get_weather_today"]


@shared_task
@logger.catch(
    reraise=True,
    message="Something goes wrong while `get_weather_today` task execution."
)
def get_weather_today():
    logger.info("Start receiving weather data.")

    weather = get_weather("today")

    logger.info("Task completed")

    return weather
