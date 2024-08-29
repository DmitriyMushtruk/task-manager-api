from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register(r"tasks", views.TaskViewSet, basename="tasks")

app_name = "task"
urlpatterns = [
    # Task routes
    path("", include(router.urls)),
]
