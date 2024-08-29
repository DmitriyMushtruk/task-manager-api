from django.contrib import admin
from django.urls import path, include

app_name = "rest_framework"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace="rest_framework")),
    path("api/", include("user.urls", "user_api")),
    path("api/", include("task.urls", "task_api"))

]
