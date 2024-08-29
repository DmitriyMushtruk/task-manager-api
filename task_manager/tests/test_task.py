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

