from flask import url_for


def test_home_route(client):
    response = client.get(url_for("home"))
    assert response.status_code == 200


def test_user_loggedin(client):
    response = client.get('/user1')
    text = response.get_data(as_text=True)
    assert "user1 logged in" in text
