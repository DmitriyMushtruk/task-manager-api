import pytest
from rest_framework.test import APIClient

from user.models import User
from task.models import Task


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


@pytest.fixture
def task_payload(user):
    return dict(
        user_id=user,
        title="Task title",
        description="Task description",
    )


@pytest.fixture
def task_user(user):
    task = Task.objects.create(
        user_id=user,
        title="Do something",
        description="Some description",
    )
    task.save()
    return task


@pytest.fixture
def task_user_completed(user):
    task = Task.objects.create(
        user_id=user,
        title="Something was already done",
        description="Some description",
        status="completed",
    )
    task.save()
    return task


@pytest.fixture
def task_second_user(second_user):
    task = Task.objects.create(
        user_id=second_user,
        title="Do something else",
        description="Some different description",
        status="in progress",
    )
    task.save()
    return task






