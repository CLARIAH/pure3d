from flask import url_for
import pytest


def test_home_route(client):
    response = client.get(url_for("home"))
    assert response.status_code == 200


@pytest.mark.parametrize("except_user1", [
    'user2',
    'user3',
    'user4'
])
def test_user1_logged_in(client, except_user1):
    response = client.get('/user1')
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "user1 logged in" in text
    assert f"{except_user1} logged in" not in text


@pytest.mark.parametrize("except_user2", [
    'user1',
    'user3',
    'user4'
])
def test_user2_logged_in(client, except_user2):
    response = client.get('/user2')
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "user2 logged in" in text
    assert f"{except_user2} logged in" not in text


@pytest.mark.parametrize("except_user3", [
    'user1',
    'user2',
    'user4'
])
def test_user3_logged_in(client, except_user3):
    response = client.get('/user3')
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "user3 logged in" in text
    assert f"{except_user3} logged in" not in text


@pytest.mark.parametrize("except_user4", [
    'user1',
    'user2',
    'user3'
])
def test_user4_logged_in(client, except_user4):
    response = client.get('/user4')
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "user4 logged in" in text
    assert f"{except_user4} logged in" not in text


@pytest.mark.parametrize("any_user", [
    'user1',
    'user2',
    'user3',
    'user4',
])
def test_no_user_logged_in(client, any_user):
    response = client.get('/home')
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert f"{any_user} logged in" not in text
