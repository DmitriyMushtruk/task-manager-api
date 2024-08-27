from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import models


class UserSerializer(serializers.ModelSerializer):
    """General User model serializer."""

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "username", "id")


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Gets and validate data that required for creating new user in database.
    """

    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=models.User.objects.all()), ],
        max_length=50,
        required=True,
    )
    password = serializers.CharField(min_length=6, write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "username", "password", "password_confirmation")

    def validate(self, data):
        """Checks if password was repeated rightly."""

        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """Create new user in database."""
        validated_data.pop("password_confirmation")
        return models.User.objects.create_user(**validated_data)
