import pytest
from rest_framework.test import APIClient

from user.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_payload():
    return dict(
        first_name="Sandor",
        last_name="Clegane",
        username="RealDog",
        password="dog_pass",
        password_confirmation="dog_pass",
    )


@pytest.fixture
def user():
    user = User.objects.create(
        first_name="Barristan",
        last_name="Selmy",
        username="RealKnight",
    )
    user.set_password("knight_pass")
    user.save()
    return user


@pytest.fixture
def second_user():
    user = User.objects.create(
        first_name="Daenerys",
        last_name="Targaryen",
        username="RealQueen",
    )
    user.set_password("queen_pass")
    user.save()
    return user


@pytest.fixture
def user_payload_access_token(user, client):
    request = client.post("/api/login/", dict(username="RealKnight", password="knight_pass", ))
    return request.data["access"]


