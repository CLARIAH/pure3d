import pytest

STATIC = "/static"
CSS = f"{STATIC}/css"
JS = f"{STATIC}/js"


@pytest.mark.parametrize(
    "file_path, expected_status_code",
    [
        (f"{STATIC}", 404),
        (f"{CSS}/style.css", 200),
        (f"{JS}/main.js", 200),
        (f"{CSS}/invalid.css", 404),
        (f"{JS}/invalid.js", 404),
        (f"{STATIC}/favicon.ico", 200),
        (f"{STATIC}/unknown.ico", 404),
    ],
)
def test_static_files(client, file_path, expected_status_code):
    response = client.get(file_path)
    assert response.status_code == expected_status_code
