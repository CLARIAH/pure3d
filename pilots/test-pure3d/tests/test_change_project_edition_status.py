import pytest

PROJECTS = "/projects"


#@pytest.mark.parametrize(
#    "key, value, type, project, expected_message",
#    [
#        (None, "root", "user", "", "Missing required form data"),
#        ("3", None, "project", "", "Missing required form data"),
#        ("1", "False", None, "2", "Missing required form data"),
#        ("2", "False", "edition", None, "Missing required form data"),
#    ],
#)
#def test_missing_values_for_update_checkpoint(
#    client, key, value, type, project, expected_message
#):
#    response = client.post(
#        "/update_data_values",
#        data={"key": key, "value": value, "type": type, "project": project},
#    )
#    assert response.status_code == 400

#    json_data = response.get_json()
#    assert json_data["success"] is False
#    assert json_data["message"] == expected_message


@pytest.mark.parametrize(
    "project, status, expected_message",
    [
        ("1", "True", "Project status of 1 is now True"),
        ("1", "False", "Project status of 1 is now False"),
        ("2", "True", "Project status of 2 is now True"),
        ("2", "False", "Project status of 2 is now False"),
        ("3", "True", "Project status of 3 is now True"),
        ("3", "False", "Project status of 3 is now False"),
    ],
)
def test_project_published_status_is_updated(client, project, status, expected_message):
    response = client.post(
        "/update_data_values",
        data={"key": project, "value": status, "type": "project", "project": " "},
    )
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["message"] == expected_message


@pytest.mark.parametrize(
    "project, status, expected_message",
    [
        ("unknown_project", "False", "Project not found"),
        ("unknown_project", "True", "Project not found"),
        ("dummy_project", "True", "Project not found"),
    ],
)
def test_invalid_project(client, project, status, expected_message):
    response = client.post(
        "/update_data_values",
        data={"key": project, "value": status, "type": "project", "project": " "},
    )
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] is False
    assert json_data["message"] == expected_message


@pytest.mark.parametrize(
    "edition, status, project, expected_message",
    [
        ("1", "True", "1", "Edition status of edition 1 in project 1 is now True"),
        ("1", "False", "1", "Edition status of edition 1 in project 1 is now False"),
        ("2", "True", "1", "Edition status of edition 2 in project 1 is now True"),
        ("2", "False", "1", "Edition status of edition 2 in project 1 is now False"),
        ("1", "True", "2", "Edition status of edition 1 in project 2 is now True"),
        ("1", "False", "2", "Edition status of edition 1 in project 2 is now False"),
        ("2", "True", "2", "Edition status of edition 2 in project 2 is now True"),
        ("2", "False", "2", "Edition status of edition 2 in project 2 is now False"),
    ],
)
def test_edition_published_status_is_updated(
    client, edition, status, project, expected_message
):
    response = client.post(
        "/update_data_values",
        data={"key": edition, "value": status, "type": "edition", "project": project},
    )
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["message"] == expected_message


@pytest.mark.parametrize(
    "edition, status, project, expected_message",
    [
        ("unknown_edition", "False", "1", "Edition not found"),
        ("unknown_edition", "True", "1", "Edition not found"),
        ("dummy_edition", "True", "1", "Edition not found"),
    ],
)
def test_invalid_edition(client, edition, status, project, expected_message):
    response = client.post(
        "/update_data_values",
        data={"key": edition, "value": status, "type": "edition", "project": project},
    )
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] is False
    assert json_data["message"] == expected_message
