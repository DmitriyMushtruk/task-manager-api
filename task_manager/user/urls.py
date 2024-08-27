from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register(r"users", views.UserListViewSet, basename="users")

app_name = "user"
urlpatterns = [
    path("", include(router.urls)),
]
