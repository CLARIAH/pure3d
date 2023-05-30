import pytest
import magic


@pytest.mark.parametrize(
    "loggedInUser",
    [
        [],
        ["costas"],
        ["susan"],
        ["kelly"],
        ["artist"],
    ],
)
def test_user_logged_in(client, loggedInUser):
    allUsers = ["costas", "susan", "kelly", "user4"]
    for user in allUsers:
        response = client.get(f"/{user}/login")
        text = response.get_data(as_text=True)
        assert response.status_code == 302  # redirect code
        if user in loggedInUser:
            assert f"{user} logged in" in text
        else:
            assert f"{user} logged in" in text
