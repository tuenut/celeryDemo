from loguru import logger
from tasks.celery import app

from libs.weather import get_weather


__all__ = ["get_weather_today"]


@app.task
@logger.catch(
    reraise=True,
    message="Something goes wrong while `get_weather_today` task execution."
)
def get_weather_today():
    logger.info("Start receiving weather data.")

    weather = get_weather("today")

    logger.info("Task completed")

    return weather
