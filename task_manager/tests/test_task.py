import pytest

"""Tests of GET method to /api/task/ endpoint"""


@pytest.mark.django_db
def test_get_task_list(
        client,
        user_payload_access_token,
        task_user,
        task_second_user
):
    """Test get list of all tasks"""

    response = client.get("/api/tasks/", HTTP_AUTHORIZATION=f"Bearer {user_payload_access_token}")

    assert response.status_code == 200
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_filter_tasks_by_user(
        client,
        user,
        user_payload_access_token,
        second_user,
        task_user,
        task_user_completed,
        task_second_user
):
    """
    Test get list of tasks of specific user.
    Request with incorrect user_id returns empty response.
    """

    users = (user, second_user)

    for specific_user in users:
        response = client.get(
            f"/api/tasks/?user_id={specific_user.id}",
            HTTP_AUTHORIZATION=f"Bearer {user_payload_access_token}"
        )

        assert response.status_code == 200

        if specific_user == user:
            assert response.data["count"] == 2
            assert len(response.data["results"]) == 2
        elif specific_user == second_user:
            assert response.data["count"] == 1
            assert len(response.data["results"]) == 1

        assert response.data["results"][0]["user_id"] == specific_user.id


@pytest.mark.django_db
def test_filter_tasks_by_status(
        client,
        user_payload_access_token,
        second_user,
        task_user,
        task_user_completed,
        task_second_user
):
    """
    Test get list of tasks filtered by status.
    Request with incorrect status returns empty response.
    """

    status_choices = ("new", "in progress", "completed")
    wrong_status_choices = ("wrong", "status", "choices")

    for status in status_choices:
        response = client.get(f"/api/tasks/?status={status}", HTTP_AUTHORIZATION=f"Bearer {user_payload_access_token}")

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1

    for status in wrong_status_choices:
        response = client.get(f"/api/tasks/?status={status}", HTTP_AUTHORIZATION=f"Bearer {user_payload_access_token}")

        assert response.status_code == 200
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0


@pytest.mark.django_db
def test_get_task_list_without_authorization(client):
    """Checks if user without authorization can get access to the task list."""

    response = client.get(f"/api/tasks/")

    assert response.status_code == 401


"""Tests of POST method to /api/task/ endpoint"""


@pytest.mark.django_db
def test_create_task_success(client, user_payload_access_token, task_payload):
    """Test if task was created correctly."""

    response = client.post(f"/api/tasks/", task_payload, HTTP_AUTHORIZATION=f"Bearer {user_payload_access_token}")

    assert response.status_code == 201
    assert response.data["title"] == task_payload["title"]
    assert response.data["description"] == task_payload["description"]
    assert response.data["status"] == "new"


@pytest.mark.django_db
def test_create_task_without_title_field(client, user_payload_access_token, task_payload):
    """Checks if user can create new task without title field."""

    task_payload.pop("title")

    response = client.post(f"/api/tasks/", task_payload, HTTP_AUTHORIZATION=f"Bearer {user_payload_access_token}")

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_task_with_wrong_status_field(client, user_payload_access_token, task_payload):
    """Checks if user can create new task with wrong status field."""

    task_payload["status"] = "wrong_status"

    response = client.post(f"/api/tasks/", task_payload, HTTP_AUTHORIZATION=f"Bearer {user_payload_access_token}")

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_task_without_authorization(client, task_payload):
    """Checks if user without authorization can create new task."""

    response = client.post(f"/api/tasks/", task_payload)

    assert response.status_code == 401


"""Tests of PUT method to /api/task/ endpoint"""


@pytest.mark.django_db
def test_update_task_success(client, user_payload_access_token, task_payload, task_user):
    """Checks successful updating of task."""

    task_payload.pop("user_id")

    response = client.put(
        f"/api/tasks/{task_user.id}/",
        task_payload,
        HTTP_AUTHORIZATION=f"Bearer {user_payload_access_token}"
    )

    assert response.status_code == 200
    assert response.data["title"] == task_payload["title"]
    assert response.data["description"] == task_payload["description"]


@pytest.mark.django_db
def test_update_task_without_title_field(client, user_payload_access_token, task_payload, task_user):
    """Checks updating task without title field."""

    task_payload.pop("user_id")
    task_payload.pop("title")

    response = client.put(
        f"/api/tasks/{task_user.id}/",
        task_payload,
        HTTP_AUTHORIZATION=f"Bearer {user_payload_access_token}"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_update_task_with_non_exist_id(client, user_payload_access_token, task_payload, task_user):
    """Checks updating task with non-exist id."""

    response = client.put(
        f"/api/tasks/{int(task_user.id * 25)}/",
        task_payload,
        HTTP_AUTHORIZATION=f"Bearer {user_payload_access_token}"
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_task_without_permissions(client, user_payload_access_token, task_payload, task_second_user):
    """Checks updating task without permissions."""

    response = client.put(
        f"/api/tasks/{task_second_user.id}/",
        task_payload,
        HTTP_AUTHORIZATION=f"Bearer {user_payload_access_token}"
    )

    assert response.status_code == 403

