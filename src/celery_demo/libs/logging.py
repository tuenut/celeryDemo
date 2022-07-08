import os
import sys

from loguru import logger
from django.http.request import HttpRequest
from django.conf import settings

from celery.app.task import Task

from functools import update_wrapper


class Logged:
    __decorated = {}
    __configured = False

    @classmethod
    def decorate(cls, obj):
        object_path = cls.get_path_name(obj)
        if object_path not in cls.__decorated:
            cls.__decorated[object_path] = cls(obj)

        return cls.__decorated[object_path]

    def __init__(self, obj):
        self._object = obj
        update_wrapper(self, obj)

    def __call__(self, *args, **kwargs):
        logger.debug(f"self={self}")
        logger.debug(f"args=<{args}>; kwargs=<{kwargs}>")

        if isinstance(args[0], Task):
            return self._call_functional_task(*args, **kwargs)
        elif isinstance(self._object, Task):
            return self._call_class_task(*args, **kwargs)
        elif isinstance(args[0], HttpRequest):
            return self._call_view(*args, **kwargs)
        else:
            return self._call_default(*args, **kwargs)

    @staticmethod
    def get_path_name(obj):
        return f"{obj.__module__}.{obj.__name__}"

    def _call_functional_task(self, task, *args, **kwargs):
        with logger.contextualize(task_id=task.request.id):
            return self._object(task, *args, **kwargs)

    def _call_class_task(self, *args, **kwargs):
        instance = self._object(*args, **kwargs)
        with logger.contextualize(task_id=instance.request.id):
            return instance

    def _call_view(self, request, *args, **kwargs):
        with logger.contextualize(is_view=True):
            return self._object(request, *args, **kwargs)

    def _call_default(self, *args, **kwargs):
        with logger.contextualize(default=True):
            return self._object(*args, **kwargs)

    @staticmethod
    def _default_log_filter(record: dict) -> bool:
        return record["extra"].get("default", False)

    @staticmethod
    def _task_log_filter(record: dict) -> bool:
        return "task_id" in record["extra"]

    @staticmethod
    def _view_log_filter(record: dict) -> bool:
        return record["extra"].get("is_view", False)

    @classmethod
    def fallback_log_filter(cls, record: dict) -> bool:
        filters = [
            log_filter_method
            for log_filter_method in dir(cls)
            if (log_filter_method.startswith("_") and
                log_filter_method.endswith("log_filter"))
        ]
        return all(map(
            lambda method_name: not getattr(cls, method_name)(record),
            filters
        ))

    @classmethod
    def _configure_logger(cls):
        if cls.__configured:
            return

        logger.info("Configuring logger...")

        # logger.remove()
        # logger.add(
        #     sys.stderr,
        #     level="DEBUG",
        #     backtrace=False,
        #     serialize=True
        # )
        os.makedirs(settings.LOG_DIR, exist_ok=True)

        logger.add(
            settings.LOG_DIR / "default.log",
            format="{time} {level} {message}",
            level=settings.LOG_LEVEL,
            backtrace=False,
            filter=cls._default_log_filter,
            serialize=True
        )
        logger.add(
            settings.LOG_DIR / "_.log",
            format="{time} {level} {message}",
            level=settings.LOG_LEVEL,
            backtrace=False,
            filter=cls.fallback_log_filter,
            serialize=True
        )
        logger.add(
            settings.LOG_DIR / "tasks.log",
            format="{time} {level} | {extra[task_id]} | {message}",
            level=settings.LOG_LEVEL,
            backtrace=False,
            filter=cls._task_log_filter,
            serialize=True
        )
        logger.add(
            settings.LOG_DIR / "views.log",
            format="{time} {level} | view={extra[is_view]} | {message}",
            level=settings.LOG_LEVEL,
            backtrace=False,
            filter=cls._view_log_filter,
            serialize=True
        )

        cls.__configured = True



Logged._configure_logger()


