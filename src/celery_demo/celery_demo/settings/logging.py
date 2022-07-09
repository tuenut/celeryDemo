import os
import sys

from loguru import logger

from libs.logging import LoggerContext

from .paths import LOG_DIR


__all__ = ["LOG_LEVEL"]

LOG_LEVEL = "DEBUG"

logger.info("Configuring logger...")
logger.remove()

os.makedirs(LOG_DIR, exist_ok=True)

logger.add(
    LOG_DIR / "default.log",
    level=LOG_LEVEL,
    backtrace=False,
    filter=LoggerContext.fallback_log_filter,
    serialize=True
)
logger.add(
    sys.stderr,
    format="{time} {level} {message}",
    level=LOG_LEVEL,
    backtrace=False,
    filter=LoggerContext.fallback_log_filter,
)

logger.add(
    LOG_DIR / "tasks.log",
    level=LOG_LEVEL,
    backtrace=False,
    filter=LoggerContext.task_log_filter,
    serialize=True
)
logger.add(
    sys.stderr,
    format="{time} {level} | {extra[task_id]} | {message}",
    level=LOG_LEVEL,
    backtrace=False,
    filter=LoggerContext.task_log_filter,
)

logger.add(
    LOG_DIR / "views.log",
    level=LOG_LEVEL,
    backtrace=False,
    filter=LoggerContext.view_log_filter,
    serialize=True
)
logger.add(
    sys.stderr,
    format="{time} {level} | {extra[request_id]} | {message}",
    level=LOG_LEVEL,
    backtrace=False,
    filter=LoggerContext.view_log_filter,
)
