def test_css_file(client):
    response = client.get("/static/style.css")
    assert response.status_code == 200


def test_js_file(client):
    response = client.get("/static/js/main.js")
    assert response.status_code == 200


def test_invalid_css_file(client):
    response = client.get("/static/invalid.css")
    assert response.status_code == 404


def test_invalid_js_file(client):
    response = client.get("/static/js/invalid.js")
    assert response.status_code == 404
