from functools import wraps
from inspect import isclass
from typing import Type, List
from uuid import uuid4

from celery.app.task import Task
from django.http.request import HttpRequest

from loguru import logger


class LoggerContext:
    """
    Should add logger context to:
     - django functional views
     - django class-based views
     - celery functional bounded tasks
     - celery class-based tasks
    """

    _is_celery_task: bool = None
    _methods: List[str] = None

    def __init__(self, _object=None, methods=None):
        self._methods = methods or []

        if isclass(_object):
            self.decorated = self._decorate_klass(_object)
        elif _object:
            self.decorated = self._decorate_function(_object)

    @classmethod
    def decorate(cls, *args, **kwargs):
        if kwargs:
            return cls(*args, **kwargs)._decorate_klass
        else:
            return cls(args[0]).decorated

    def _decorate_klass(self, klass: Type[Task]):
        self._is_celery_task = issubclass(klass, Task)

        if self._is_celery_task and "run" not in self._methods:
            self._methods.append("run")

        if not self._methods:
            raise Exception("You should pass methods names, which you want"
                            " logging with context")

        @wraps(klass)
        def klass_wrapper(*args, **kwargs):
            instance = klass(*args, **kwargs)
            self.__decorate_instance_methods(instance)
            return instance

        return klass_wrapper

    def __decorate_instance_methods(self, instance):
        for method_name in self._methods:
            method = getattr(instance, method_name)
            wrapped_method = self._decorate_function(method)
            setattr(instance, method_name, wrapped_method)

    def _decorate_function(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if self._is_celery_task:
                return self.__run_task(fn, *args, **kwargs)

            elif args and isinstance(args[0], Task):
                return self.__call_task(fn, *args, **kwargs)

            elif args and isinstance(args[0], HttpRequest):
                return self.__call_view(fn, *args, **kwargs)

            else:
                return fn(*args, **kwargs)

        return wrapper

    @staticmethod
    def __call_task(fn, task: Task, *args, **kwargs):
        with logger.contextualize(task_id=task.request.id):
            return fn(task, *args, **kwargs)

    @staticmethod
    def __run_task(fn, *args, **kwargs):
        with logger.contextualize(task_id=fn.__self__.request.id):
            return fn(*args, *kwargs)

    @staticmethod
    def __call_view(view, request: HttpRequest, *args, **kwargs):
        with logger.contextualize(request_id=uuid4()):
            return view(request, *args, **kwargs)

    @staticmethod
    def get_path_name(obj):
        """Can be used to log into separated files each logged object"""
        return f"{obj.__module__}.{obj.__name__}"

    @staticmethod
    def view_log_filter(record: dict) -> bool:
        return "request_id" in record["extra"]

    @staticmethod
    def task_log_filter(record: dict) -> bool:
        return "task_id" in record["extra"]

    @classmethod
    def fallback_log_filter(cls, record: dict) -> bool:
        return all(map(lambda method: not method(record), cls.filters))

    filters = [view_log_filter, task_log_filter]
