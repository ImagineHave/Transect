import pytest
from flask import g, session
from transect.db import get_db

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )

    with app.app_context():
        assert get_db()['users'].find_one({'username':'a'}) is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data
    
def test_login(client, app, auth):
    assert client.get('/auth/login').status_code == 200
    auth.login()
    
    with app.app_context():
        user = get_db()['users'].find_one({'username':'test'})
        userid = str(user['_id'])

    with client:
        client.get('/')
        assert session['user_id'] == userid
        assert g.username == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'invalid details.'),
    ('test', 'a', b'invalid details.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
    
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session