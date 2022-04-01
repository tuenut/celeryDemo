from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET

from libs.tasks import get_task_result
from .tasks import notify_user_in_slack


__all__ = ["send_notification_view", "notify_result_view"]


@require_POST
def send_notification_view(request):
    username = request.POST["user"]
    result = notify_user_in_slack.delay(username)
    return redirect("notify:result", task_id=result.id)


@require_GET
def notify_result_view(request, task_id):
    task_result = get_task_result(task_id)

    return render(request, "result.html", context=task_result)
