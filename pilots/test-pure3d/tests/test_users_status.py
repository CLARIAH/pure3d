#import magic


def test_users_route(client):
    response = client.get('/users')

    assert response.status_code == 200
    assert b"<h1>User Roles</h1>" in response.data


def test_update_user_role(client):
    response = client.post(
        "/update_data_values", data={"key": "susan", "value": "admin", "update_type": "user", "project": " "}
    )
    assert response.status_code == 200
    assert response.json == {"success": True}

    # Verify that the user role has been updated
    response = client.get("/users")
    assert response.status_code == 200
    assert b'<td>susan</td>' in response.data
    assert b'<td id="susan">' in response.data
    assert b'<span class="value">admin</span>' in response.data


def test_invalid_update_type(client):
    response = client.post(
        "/update_user_role", data={"key": "susan", "value": "admin", "update_type": "dummy", "project": " "}
    )
    assert response.status_code == 200
    assert response.json == {"success": False, "error": "Invalid update type"}


#def test_invalid_user(client):
    #response = client.post(
        #"/update_data_values", data={"key": "dummy", "value": "user", "type": "user"}
    #)
    #assert response.status_code == 200
    #assert response.json == {"success": False, "error": "User not found"}


#def test_invalid_user_role(client):
    #response = client.post(
        #"/update_data_values", data={"key": "susan", "value": "dummy", "type": "user"}
    #)
    #assert response.status_code == 200
    #assert response.json == {"success": False, "error": "User role not valid"}
