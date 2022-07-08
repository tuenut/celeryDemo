import os, sys
from inspect import isclass

from typing import Type

from uuid import uuid4

from loguru import logger
from django.http.request import HttpRequest
from django.conf import settings

from celery.app.task import Task

from functools import wraps, update_wrapper


def get_path_name(obj):
    """Can be used to log into separated files each logged object"""
    return f"{obj.__module__}.{obj.__name__}"


def _view_log_filter(record: dict) -> bool:
    return "request_id" in record["extra"]


def _task_log_filter(record: dict) -> bool:
    return "task_id" in record["extra"]


def _fallback_log_filter(record: dict) -> bool:
    filters = [_view_log_filter, _task_log_filter]
    return all(map(lambda method: not method(record), filters))


logger.info("Configuring logger...")
logger.remove()

os.makedirs(settings.LOG_DIR, exist_ok=True)

logger.add(
    settings.LOG_DIR / "default.log",
    level=settings.LOG_LEVEL,
    backtrace=False,
    filter=_fallback_log_filter,
    serialize=True
)
logger.add(
    sys.stderr,
    format="{time} {level} {message}",
    level=settings.LOG_LEVEL,
    backtrace=False,
    filter=_fallback_log_filter,
)

logger.add(
    settings.LOG_DIR / "tasks.log",
    level=settings.LOG_LEVEL,
    backtrace=False,
    filter=_task_log_filter,
    serialize=True
)
logger.add(
    sys.stderr,
    format="{time} {level} | {extra[task_id]} | {message}",
    level=settings.LOG_LEVEL,
    backtrace=False,
    filter=_task_log_filter,
)

logger.add(
    settings.LOG_DIR / "views.log",
    level=settings.LOG_LEVEL,
    backtrace=False,
    filter=_view_log_filter,
    serialize=True
)
logger.add(
    sys.stderr,
    format="{time} {level} | {extra[request_id]} | {message}",
    level=settings.LOG_LEVEL,
    backtrace=False,
    filter=_view_log_filter,
)


class LoggerContext:
    """
    Should add logger context to:
     - django functional views
     - django class-based views
     - celery functional bounded tasks
     - celery class-based tasks

     Class-based decorator not works with celery functional bounded tasks.
      Seems like kwargs for @shared_task(bind=True) ignored, or somehow `self`
      not passed to class-based decorator instance __call__.
    """

    def __init__(self, obj):
        self._object = obj
        self._decorated = self.decorate(obj)

        update_wrapper(self, obj)

    def __call__(self, *args, **kwargs):
        return self._decorated(*args, **kwargs)

    @classmethod
    def decorate(cls, obj):
        if isclass(obj) and issubclass(obj, Task):
            return cls._decorate_klass_task(obj)
        else:
            return cls._decorate_function(obj)

    @classmethod
    def _decorate_klass_task(cls, klass: Type[Task]):
        @wraps(klass)
        def klass_wrapper(*args, **kwargs):
            instance = klass(*args, **kwargs)
            run_method = instance.run

            @wraps(run_method)
            def run_wrapper(*method_args, **method_kwargs):
                return cls.__call_functional_task(
                    run_method, instance, *args, **kwargs
                )

            instance.run = run_wrapper

            return instance

        return klass_wrapper

    @classmethod
    def _decorate_function(cls, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if args and isinstance(args[0], Task):
                return cls.__call_functional_task(fn, *args, **kwargs)

            elif args and isinstance(args[0], HttpRequest):
                return cls.__call_view(fn, *args, **kwargs)

            else:
                return fn(*args, **kwargs)

        return wrapper

    @staticmethod
    def __call_functional_task(fn, self: Task, *args, **kwargs):
        with logger.contextualize(task_id=self.request.id):
            return fn(self, *args, **kwargs)

    @staticmethod
    def __call_view(view, request: HttpRequest, *args, **kwargs):
        with logger.contextualize(request_id=uuid4()):
            return view(request, *args, **kwargs)
