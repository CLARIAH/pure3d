from flask import url_for

def test_home_route(client):
    response = client.get(url_for('home'))
    assert response.status_code == 200
    assert b"user1" in response.data
    
def test_user_loggedin(client):
    response = client.get('/user1') 
    assert response.status_code == 200
    assert b"user1" in response.data
    assert b"This is user1" in response.data
