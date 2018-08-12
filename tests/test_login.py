import pytest
from flask import g, session
from transect.db import get_db


def test_login(client, app, auth):
    ''' redirect '''
    assert client.get('/').status_code == 302
    
    ''' login '''
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'login' in response.data
    assert b'register' in response.data
    
    response = auth.login()
    assert response.status_code == 200
    
    ''' home page with logout '''
    response = client.get('/')
    assert client.get('/').status_code == 200
    assert b'logout' in response.data
    