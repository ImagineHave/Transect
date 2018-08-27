from flask import g, session
from tests.conftest import USERNAME1


def test_logout(client, auth, test_user):
    with client:
        response = auth.login()
        assert response.status_code == 200
        assert b'home' in response.data
        assert b'login' not in response.data
        assert b'register' not in response.data
        assert session['user_id'] == test_user.get_user_id()
        assert g.username == USERNAME1
        response = auth.logout()
        assert b'home' not in response.data
        assert b'login' in response.data
        assert b'register' in response.data
        assert 'user_id' not in session
        assert g.username != USERNAME1
