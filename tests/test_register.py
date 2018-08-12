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