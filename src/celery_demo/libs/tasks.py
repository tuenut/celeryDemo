from celery.result import AsyncResult, TimeoutError


def get_task_result(task_id: str) -> dict:
    async_result = AsyncResult(task_id)
    status = async_result.ready()
    try:
        result = async_result.get(timeout=1, propagate=False)
    except TimeoutError:
        result = None

    return {
        "status": status,
        "result": result,
        "task_name": async_result.name
    }
