import pytest
from flask import g, session
from transect.db import get_db


def test_register(client, app, auth, test_user):
    with client:
        username = "t3st"
        password = "somePassword"
        email = "some@email.com"
        ''' attempt login '''
        data = {'username': username, 'password': password}
        response = auth.login(data)
        message = b'invalid details.'
        assert message in response.data

        ''' exists '''
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'value="register"' in response.data

        ''' register '''
        data = {'username': username, 'password': password, 'confirm': password, 'email': email}
        response = auth.register(data)
        assert response.status_code == 200
        assert b'login' in response.data
        assert b'register' in response.data

        with app.app_context():
            user = get_db()['users'].find_one({'username': username})
            assert user is not None
            user_id = str(user['_id'])

        data = {'username': username, 'password': password}
        response = auth.login(data)
        assert response.status_code == 200
        assert b'home' in response.data
        assert b'login' not in response.data
        assert b'register' not in response.data
        assert session['user_id'] == user_id
        assert g.username == username


@pytest.mark.parametrize(('username', 'password', 'confirm', 'email', 'message'), (
        ('', 'test', 'test', 'email@email.com', b'username required.'),
        ('test', '', 'test', 'email@email.com', b'password required.'),
        ('test', 'test', 'test1', 'email@email.com', b'passwords must match.'),
        ('test', 'test', 'test', '', b'email address required.'),
        ('test', 'test', 'test', '3453', b'email address required.'),
))
def test_login_validate_input(auth, username, password, confirm, email, message):
    data = {'username': username, 'password': password, 'confirm': confirm, 'email': email}
    response = auth.register(data)
    assert message in response.data
