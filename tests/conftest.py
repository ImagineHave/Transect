import os
import pytest
from transect import create_app
from transect.db import get_db, init_db
from werkzeug.security import check_password_hash, generate_password_hash


@pytest.fixture
def app():
    
    app = create_app({'TESTING': True, 'WTF_CSRF_ENABLED':False})
    
    with app.app_context():
        init_db()
    
    with app.app_context():
        get_db()['users'].insert_one({"username":'test',"password":generate_password_hash('test')})
        get_db()['users'].insert_one({"username":'test1',"password":generate_password_hash('test1')})
    
    yield app
    
    
@pytest.fixture
def client(app):
    return app.test_client()
    
@pytest.fixture
def runner(app):
    return app.test_cli_runner()
    
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

class TestUser(object):
    def __init__(self, app):
        self.app = app
        
    def getUserid(self, username='test'):
        with self.app.app_context():
            return str(get_db()['users'].find_one({"username":'test'})['_id'])
            
    def getUsername(self, username='test'):
        with self.app.app_context():
            return get_db()['users'].find_one({"username":'test'})['username']
    
@pytest.fixture
def testUser(app):
    return TestUser(app)