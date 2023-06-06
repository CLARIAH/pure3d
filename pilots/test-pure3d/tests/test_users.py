import pytest


@pytest.mark.parametrize(
    "TestUsers",
    [
        [],
        ["costas"],
        ["susan"],
        ["kelly"],
        ["artist"],
    ],
)
def test_user_login(client, TestUsers):
    allUsers = ["costas", "susan", "kelly", "artist"]
    for user in allUsers:
        response = client.get(f"/{user}/login")
        assert response.status_code == 302  # redirect code

        # Verify that the user has been logged in
        if user in TestUsers:
            assert response.headers.get("X-Comment").strip() == f"{user} logged in"
            with client.session_transaction() as session:
                assert session["user"] == user
        else:
            assert user not in TestUsers

        # Verify the redirection target
        assert response.location == "/home"


def test_user_logout(client):
    # Log in a user first
    response = client.get("/testuser/login")
    assert response.status_code == 302  # redirect code

    # Verify the session variables after login
    with client.session_transaction() as session:
        assert session["user"] == "testuser"
        assert "is logged in" in session["user_text"]

    # Perform logout
    response = client.get("/logout")
    assert response.status_code == 302  # redirect code

    # Verify the session variables after logout
    with client.session_transaction() as session:
        assert session.get("user") is None
        assert session.get("user_text") is None
