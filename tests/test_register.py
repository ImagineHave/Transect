import pytest
from flask import g, session
from transect.db import get_db


def test_register(client, app, auth):
    assert client.get('/auth/register').status_code == 200
    
    username = "t3st"
    password = "somePassword"
    email = "some@email.com"
    
    response = auth.register(username,password,email)
    
    print(response.data)

    with app.app_context():
        assert get_db()['users'].find_one({'username':username}) is not None