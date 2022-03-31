from django.urls import path

from .views import *
from .apps import MathDemoConfig


app_name = MathDemoConfig.name

urlpatterns = [
    path("", main_page, name="main-page"),
    path("result/<str:task_id>", result_view, name="math-result"),
    path("add/", add_task_view, name="add-request"),
    path("sub/", sub_task_view, name="sub-request"),
    path("mul/", mul_task_view, name="mul-request"),
    path("divide/", divide_task_view, name="divide-request"),
    path("xsum/", xsum_task_view, name="xsum-request"),
]
