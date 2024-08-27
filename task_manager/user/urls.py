from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

router = SimpleRouter()

router.register(r"users", views.UserListViewSet, basename="users")
router.register(r"register", views.RegisterUserViewSet, basename="registrations")

app_name = "user"
urlpatterns = [
    # User routes
    path("", include(router.urls)),

    # JWT tokens routes
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
