from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet,ViewSet

from . import models

from . import serializers


class UserListViewSet(ListModelMixin, GenericViewSet):
    """
    Returns list of all users OR specific user if query
    param 'username' was given.
    """

    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = models.User.objects.all()
        username = self.request.query_params.get("username")
        if username:
            queryset = queryset.filter(username=username)
        return queryset
