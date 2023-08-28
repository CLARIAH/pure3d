import pytest


@pytest.mark.parametrize(
    "key, value, expected_message",
    [
        ("invalid_user", "admin", "Invalid user"),
        ("unknown_user", "guest", "Invalid user"),
        ("artist", "unknown_user_role", "Invalid user role"),
        ("kelly", "invalid_user_role", "Invalid user role"),
    ],
)
def test_invalid_user_or_user_role(client, key, value, expected_message):
    response = client.post(
        "/update_data_values",
        data={"key": key, "value": value, "type": "user", "project": ""},
    )
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] is False
    assert json_data["message"] == expected_message


@pytest.mark.parametrize(
    "key, value, expected_message",
    [
        ("susan", "admin", "status of susan has changed to admin"),
        ("susan", "guest", "status of susan has changed to guest"),
        ("susan", "user", "status of susan has changed to user"),
        ("susan", "root", "status of susan has changed to root"),
        ("costas", "admin", "status of costas has changed to admin"),
        ("costas", "guest", "status of costas has changed to guest"),
        ("costas", "user", "status of costas has changed to user"),
        ("costas", "root", "status of costas has changed to root"),
    ],
)
def test_user_role_is_updated(client, key, value, expected_message):
    response = client.post(
        "/update_data_values",
        data={"key": key, "value": value, "type": "user", "project": " "},
    )
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["message"] == expected_message


@pytest.mark.parametrize(
    "key, value",
    [
        ("susan", "admin"),
        ("susan", "guest"),
        ("artist", "user"),
        ("artist", "root"),
    ],
)
def test_invalid_update_type(client, key, value):
    response = client.post(
        "/update_data_values",
        data={"key": key, "value": value, "type": "invalid type", "project": ""},
    )
    assert response.json == {"success": False, "error": "Invalid update type"}
