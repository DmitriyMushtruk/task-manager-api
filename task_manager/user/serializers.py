from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "username", "id")
