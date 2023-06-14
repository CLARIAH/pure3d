def test_home(client):
    for url in ["/", "/home"]:
        response = client.get(url)

    assert response.status_code == 200


def test_users(client):
    response = client.get("/users")

    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "Users of Pure3D" in text


def test_projects(client):
    response = client.get("/projects")

    assert response.status_code == 200
