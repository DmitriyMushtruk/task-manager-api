from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    """Authorization User Model."""

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.TextField(max_length=50, unique=True)
    password = models.CharField(validators=[MinLengthValidator(6)])

    def __str__(self):
        return self.username

