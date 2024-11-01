import string
import secrets


def test_url_does_not_exists(client):
    length = 8
    characters = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(characters) for _ in range(length))
    response = client.get(f"/{random_string}")
    assert response.status_code == 404


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
