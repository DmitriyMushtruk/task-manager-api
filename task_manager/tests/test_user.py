import pytest
from rest_framework.exceptions import ErrorDetail

"""Tests of /api/register/ endpoint."""


@pytest.mark.django_db
def test_register_successful(client, user_payload):
    """Testing successful registration action."""

    response = client.post("/api/register/", user_payload)
    data = response.data

    assert data["first_name"] == user_payload["first_name"]
    assert data["last_name"] == user_payload["last_name"]
    assert data["username"] == user_payload["username"]
    assert "password" not in data
    assert "password_confirmation" not in data


@pytest.mark.django_db
def test_register_all_fields_missing(client, user_payload):
    """
    Checks that each required field was given.
    Return appropriate error message for each missed field.
    """

    response = client.post("/api/register/", {})

    expected_response_data = user_payload.copy()
    expected_response_data.update(
        (key, [ErrorDetail(string='This field is required.', code='required')])
        for key in expected_response_data
    )

    assert response.status_code == 400
    assert response.data == expected_response_data


@pytest.mark.django_db
def test_register_all_fields_empty(client, user_payload):
    """
    Checks that each field is not blank (empty).
    Return appropriate error message for each empty field.
    """

    blank_fields_user_payload = user_payload.copy()
    blank_fields_user_payload.update((key, '') for key in blank_fields_user_payload)

    response = client.post("/api/register/", blank_fields_user_payload)

    expected_response_data = user_payload.copy()
    expected_response_data.update(
        (key, [ErrorDetail(string='This field may not be blank.', code='blank')])
        for key in expected_response_data
    )

    assert response.status_code == 400
    assert response.data == expected_response_data


@pytest.mark.django_db
def test_register_short_password(client, user_payload):
    """Checks password min length validation."""

    short_pass_payload = user_payload.copy()
    short_pass_payload["password"] = "short"

    response = client.post("/api/register/", short_pass_payload)

    assert response.status_code == 400
    assert "password" in response.data
    assert "Ensure this field has at least 6 characters." in response.data["password"][0]


@pytest.mark.django_db
def test_register_unique_username(client, user, user_payload):
    """Checks username unique validation."""

    copy_username_payload = user_payload.copy()
    copy_username_payload["username"] = "RealKnight"

    response = client.post("/api/register/", copy_username_payload)

    assert response.status_code == 400
    assert "username" in response.data
    assert "This field must be unique." in response.data["username"][0]


@pytest.mark.django_db
def test_register_password_confirmation(client, user_payload):
    """Checks that fields 'password' and 'password_confirmation' are equal."""

    wrong_pass_confirmation_payload = user_payload.copy()
    wrong_pass_confirmation_payload["password_confirmation"] = "wrong_pass"

    response = client.post("/api/register/", wrong_pass_confirmation_payload)

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert "Passwords do not match." in response.data["non_field_errors"][0]


"""Tests of /api/login/ endpoint."""


@pytest.mark.django_db
def test_login_successful(client, user):
    """Test successful login action."""

    response = client.post("/api/login/", dict(username=user.username, password="knight_pass"))

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_wrong_credentials(client, user):
    """Checks login fails when an incorrect username and pass were given."""

    response = client.post("/api/login/", dict(username=user.username.capitalize(), password="wrong_pass"))

    assert response.status_code == 401
    assert response.data["detail"] == "No active account found with the given credentials"


@pytest.mark.django_db
def test_login_all_fields_missing(client):
    """
    Checks if both username and pass were given.
    """

    response = client.post("/api/login/", {})

    assert response.status_code == 400
    assert response.data["username"][0] == "This field is required."
    assert response.data["password"][0] == "This field is required."


@pytest.mark.django_db
def test_login_all_fields_empty(client):
    """
    Checks if both username and pass are not blank (empty).
    """

    response = client.post("/api/login/", dict(username="", password=""))

    assert response.status_code == 400
    assert response.data["username"][0] == "This field may not be blank."
    assert response.data["password"][0] == "This field may not be blank."

