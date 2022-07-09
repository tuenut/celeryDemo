from loguru import logger


from celery_demo.celery import app
from libs.logging import LoggerContext


__all__ = ["notify_user_in_slack"]

from libs.requests import request


@LoggerContext.decorate
class UserNotificationTask(app.Task):
    @logger.catch(
        reraise=True,
        message="Something goes wrong while `notify_user_in_slack` task execution."
    )
    def run(self, user):
        logger.info(f"Start sending notification to slack for user <{user}>.")

        request()

        logger.info("Task completed.")


notify_user_in_slack = app.register_task(UserNotificationTask())
