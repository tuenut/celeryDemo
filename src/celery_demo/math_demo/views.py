from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET

from libs.tasks import get_task_result
from .tasks import (
    add_request, sub_request, mul_request, divide_request, xsum_request
)


__all__ = [
    "add_task_view", "sub_task_view", "mul_task_view", "divide_task_view",
    "xsum_task_view", "main_page", "result_view"
]


@require_GET
def main_page(request):
    return render(request, template_name="math/index.html")


def _extract_x_and_y(request):
    return int(request.POST["x"]), int(request.POST["y"])


@require_POST
def add_task_view(request):
    x, y = _extract_x_and_y(request)
    result = add_request.delay(x, y)

    return redirect("math:math-result", task_id=result.id)


@require_POST
def sub_task_view(request):
    x, y = _extract_x_and_y(request)
    result = sub_request.delay(x, y)

    return redirect("math:math-result", task_id=result.id)


@require_POST
def mul_task_view(request):
    x, y = _extract_x_and_y(request)
    result = mul_request.delay(x, y)

    return redirect("math:math-result", task_id=result.id)


@require_POST
def divide_task_view(request):
    x, y = _extract_x_and_y(request)
    result = divide_request.delay(x, y)

    return redirect("math:math-result", task_id=result.id)


@require_POST
def xsum_task_view(request):
    numbers = request.POST["numbers"].split()
    result = xsum_request.delay(numbers)

    return redirect("math:math-result", task_id=result.id)


@require_GET
def result_view(request, task_id):
    task_result = get_task_result(task_id)

    return render(request, "result.html", context=task_result)
