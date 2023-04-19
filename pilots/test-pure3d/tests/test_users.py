import pytest


@pytest.mark.parametrize(
    "loggedInUser",
    [
        [],
        ["user1"],
        ["user2"],
        ["user3"],
        ["user4"],
    ],
)
def test_user_logged_in(client, loggedInUser):
    allUsers = ["user1", "user2", "user3", "user4"]
    for user in allUsers:
        response = client.get(f"/{user}/login")
        text = response.get_data(as_text=True)
        assert response.status_code == 200
        if user in loggedInUser:
            assert f"{user} logged in" in text
        else:
            assert f"{user} logged in" in text
