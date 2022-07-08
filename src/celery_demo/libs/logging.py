import os

from loguru import logger
from django.http.request import HttpRequest
from django.conf import settings
from django.utils.decorators import method_decorator, partial

from celery.app.task import Task

from inspect import isclass
from functools import wraps


class Logged:
    __configured = False

    @classmethod
    def decorate(cls, obj):
        logger.debug(f"Get object to logger decoration: {obj}")
        if isclass(obj):
            return cls._get_class_wrapper(obj)
        else:
            return cls._get_functional_wrapper(obj)

    @staticmethod
    def get_path_name(obj):
        return f"{obj.__module__}.{obj.__name__}"

    @classmethod
    def _get_functional_wrapper(cls, fn_object):
        logger.debug(f"Decorate {fn_object} as function-object.")

        @wraps(fn_object)
        def wrapper(*args, **kwargs):
            if args and isinstance(args[0], Task):
                return cls._call_functional_task(fn_object, *args, **kwargs)

            elif args and isinstance(args[0], HttpRequest):
                return cls._call_view(fn_object, *args, **kwargs)

            else:
                return cls._default_call(fn_object, *args, **kwargs)

        return wrapper

    @classmethod
    def _get_class_wrapper(cls, klass):
        logger.debug(f"Decorate {klass} as class-object.")

        if issubclass(klass, Task):
            logger.debug(f"Decorate as celery Task.")

            @wraps(klass)
            def klass_wrapper(*args, **kwargs):
                _partial_call = partial(cls._call_functional_task, klass.run)
                logger.debug(f"Got partial functional caller for `run` method: {_partial_call}")

                _run_decorator = method_decorator(name="run", decorator=_partial_call)
                logger.debug(f"Got method decorator for `run` method: {_run_decorator}")

                _klass = _run_decorator(klass)
                logger.debug(f"Got decorated Task class: {_klass}")

                task_instance = _klass(*args, **kwargs)
                logger.debug(f"Got decorated class instance: {task_instance}")

                return task_instance

            return klass_wrapper

        else:
            logger.debug("Decorate class with default caller.")

            @wraps(klass)
            def wrapper(*args, **kwargs):
                return cls._default_call(*args, **kwargs)

            return wrapper

    @staticmethod
    def _call_functional_task(task_function, task, *args, **kwargs):
        with logger.contextualize(task_id=task.request.id):
            return task_function(task, *args, **kwargs)

    @staticmethod
    def _call_task_class(task_klass, *args, **kwargs):
        instance = task_klass(*args, **kwargs)

        with logger.contextualize(task_id=instance.request.id):
            return instance

    @staticmethod
    def _call_view(view, request, *args, **kwargs):
        with logger.contextualize(is_view=True):
            return view(request, *args, **kwargs)

    @staticmethod
    def _default_call(obj, *args, **kwargs):
        with logger.contextualize(default=True):
            return obj(*args, **kwargs)

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

        os.makedirs(settings.LOG_DIR, exist_ok=True)

        logger.add(
            settings.LOG_DIR / "_.log",
            format="{time} {level} {message}",
            level=settings.LOG_LEVEL,
            backtrace=False,
            filter=cls.fallback_log_filter,
            serialize=True
        )
        logger.add(
            settings.LOG_DIR / "default.log",
            format="{time} {level} {message}",
            level=settings.LOG_LEVEL,
            backtrace=False,
            filter=cls._default_log_filter,
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
