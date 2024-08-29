from rest_framework import serializers

from . import models


class TaskSerializer(serializers.ModelSerializer):
    """General Task model serializer."""

    class Meta:
        model = models.Task
        fields = '__all__'
        read_only_fields = ['user_id']

