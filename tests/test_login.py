import pytest
from flask import g, session
from transect.db import get_db


def test_login(client, app, auth, testUser):
    with client:
        ''' redirect '''
        assert client.get('/').status_code == 302
        
        ''' login '''
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'login' in response.data
        assert b'register' in response.data
        
        response = client.post('/auth/login',data={'username': 'test', 'password': 'test'})
        assert response.status_code == 200
        print(session)
        
        ''' home page with logout '''
        response = client.get('/')
        response.status_code == 200
        print(session)
        assert session['userid'] == testUser.getUserid()
        assert g.username == 'test'
    
    
    
    print(response.status_code)
    print(response.data)
    
    assert response.status_code == 200
    assert b'logout' in response.data
    