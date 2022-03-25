from loguru import logger
from tasks.celery import app

from libs.weather import get_weather


__all__ = ["get_weather_today"]


@app.task
def get_weather_today():
    logger.info("Start receiving weather data.")

    try:
        weather = get_weather("today")
    except:
        logger.exception("Something goes wrong while task execution.")
        raise
    else:
        logger.info("Task completed")

    return weather
