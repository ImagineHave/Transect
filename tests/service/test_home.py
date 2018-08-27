from flask import g, session
from tests.conftest import USERNAME1


def test_home(client, app, auth, test_user):
    with client:
        ''' redirect '''
        response = client.get('/', follow_redirects=True)
        assert b'value="login"' in response.data

        ''' login '''
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'login' in response.data
        assert b'register' in response.data

        response = auth.login()
        assert response.status_code == 200
        assert b'login' not in response.data
        assert b'register' not in response.data
        assert b'home' in response.data
        assert b'transactions' in response.data
        assert b'series' in response.data
        assert session['user_id'] == test_user.get_user_id()
        assert g.username == USERNAME1
