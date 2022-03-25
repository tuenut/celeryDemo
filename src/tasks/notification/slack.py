from loguru import logger

from libs.requests import request
from tasks.celery import app


__all__ = ["notify_user_in_slack"]


@app.task
@logger.catch(
    reraise=True,
    message="Something goes wrong while `notify_user_in_slack` task execution."
)
def notify_user_in_slack(user):
    logger.info(f"Start sending notification to slack for user <{user}>.")

    request()

    logger.info("Task completed.")
