from loguru import logger

from celery import shared_task


__all__ = ["notify_user_in_slack"]

from libs.requests import request


@shared_task
@logger.catch(
    reraise=True,
    message="Something goes wrong while `notify_user_in_slack` task execution."
)
def notify_user_in_slack(user):
    logger.info(f"Start sending notification to slack for user <{user}>.")

    request()

    logger.info("Task completed.")
