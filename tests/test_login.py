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
        
        response = client.post('/auth/login', data={'username':'test','password':'test'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'home' in response.data
        assert b'login' not in response.data
        assert b'register' not in response.data
        
        ''' home page with logout '''
        response = client.get('/')
        response.status_code == 200
        assert session['userid'] == testUser.getUserid()
        assert g.username == 'test'
    
    
    
    print(response.status_code)
    print(response.data)
    
    assert response.status_code == 200
    assert b'logout' in response.data
    