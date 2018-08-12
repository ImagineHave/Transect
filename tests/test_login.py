import pytest
from flask import g, session
from transect.db import get_db


def test_login(client, app, auth, testUser):
    with client:
        ''' redirect '''
        response = client.get('/', follow_redirects=True)
        assert b'value="login"' in response.data
        
        ''' login '''
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'login' in response.data
        assert b'register' in response.data
        print(response.data)
        
        response = auth.login()
        assert response.status_code == 200
        assert b'home' in response.data
        assert b'login' not in response.data
        assert b'register' not in response.data
        assert session['userid'] == testUser.getUserid()
        assert g.username == 'test'
        

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'invalid logon details.'),
    ('test', 'a', b'invalid logon details.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
    