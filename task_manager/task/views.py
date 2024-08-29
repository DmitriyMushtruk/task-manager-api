from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from . import models

from . import serializers

from . import permissions


class TaskListPagination(PageNumberPagination):
    page_size = 8
    page_query_param = "page_size"
    max_page_size = 10


class TaskViewSet(ModelViewSet):
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwnerOrReadOnly]
    pagination_class = TaskListPagination

    def get_queryset(self):
        """
        Returns list of all tasks if query params were not given.
        Otherwise, returns queryset that was filtered using query params.
        Allows to filter task list by fields: user_id, status.
        """

        queryset = models.Task.objects.all().order_by("status")

        filter_params = {}
        for param in ['user_id', 'status']:
            value = self.request.query_params.get(param)
            if value:
                filter_params[param] = value

        if filter_params:
            queryset = queryset.filter(**filter_params).order_by("status")

        return queryset

    def perform_create(self, serializer):
        """Automatically adds user_id field on task data with creating new task."""

        serializer.save(user_id=self.request.user)

    def perform_update(self, serializer):
        """
        Override perform_update method.
        If 'completed' param was given changes field 'status' of task into 'completed'.
        """

        if "completed" in self.request.query_params:
            serializer.save(status="completed", partial=True)
        else:
            serializer.save()
