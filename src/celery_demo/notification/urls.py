from django.urls import path

from .views import send_notification_view, notify_result_view
from .apps import NotificationConfig


app_name = NotificationConfig.name

urlpatterns = [
    path("", send_notification_view, name="send"),
    path("<str:task_id>", notify_result_view, name="result")
]
