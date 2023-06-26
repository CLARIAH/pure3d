import pytest

PROJECTS = "/projects"


# @pytest.mark.parametrize(
# "file_path", "expected_status_code",
# [
# (f"{PROJECTS}/4rbhui3fGYy743I", 500),
# ],
# )
# def test_unexpected_project_urls(client, file_path, expected_status_code):
# response = client.get(file_path)
# assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "key, value, expected_message",
    [
        ("1", "True", "project status of 1 is now True"),
        ("1", "False", "project status of 1 is now False"),
        ("2", "True", "project status of 2 is now True"),
        ("2", "False", "project status of 2 is now False"),
        ("3", "True", "project status of 3 is now True"),
        ("3", "False", "project status of 3 is now False"),
    ],
)
def test_project_published_status_is_updated(client, key, value, expected_message):
    response = client.post(
        "/update_data_values",
        data={"key": key, "value": value, "type": "project", "project": " "},
    )
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["message"] == expected_message


@pytest.mark.parametrize(
    "key, value, expected_message",
    [
        ("unknown_project", "False", "Project not found"),
        ("unknown_project", "True", "Project not found"),
        ("dummy_project", "True", "Project not found"),
    ],
)
def test_invalid_user_or_user_role(client, key, value, expected_message):
    response = client.post(
        "/update_data_values",
        data={"key": key, "value": value, "type": "project", "project": " "},
    )
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] is False
    assert json_data["message"] == expected_message
