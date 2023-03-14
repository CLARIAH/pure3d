import pytest


@pytest.mark.parametrize("user1_projects", [
    '25 Northumberland Road',
    'Clanwilliam House'
])
def test_check_user1_projects(client, user1_projects):
    response = client.get('/user1/projects')
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert f"{user1_projects}" in text


@pytest.mark.parametrize("user2_projects", [
    'User2 - Project1',
    'User2 - Project2',
    'User2 - Project3',
    'User2 - Project4'
])
def test_check_user2_projects(client, user2_projects):
    response = client.get('/user2/projects')
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert f"{user2_projects}" in text


@pytest.mark.parametrize("user3_projects", [
    'User3 - Project1',
    'User3 - Project2'
])
def test_check_user3_projects(client, user3_projects):
    response = client.get('/user3/projects')
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert f"{user3_projects}" in text


@pytest.mark.parametrize("user4_projects", [
    'User4 - Project1',
    'User4 - Project2'
])
def test_check_user4_projects(client, user4_projects):
    response = client.get('/user4/projects')
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert f"{user4_projects}" in text