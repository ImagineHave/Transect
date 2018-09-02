import pytest
import os
from transect import create_app
from transect.db import get_db, init_db
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from datetime import datetime

USERNAME1 = 'username1'
USERNAME2 = 'username2'
PASSWORD1 = 'password1'
PASSWORD2 = 'password2'
EMAIL1 = 'e1@ma.il'
EMAIL2 = 'e2@ma.il'

USER1 = {
    "username": USERNAME1,
    "password": PASSWORD1,
    "email": EMAIL1
}

USER2 = {
    "username": USERNAME2,
    "password": PASSWORD2,
    "email": EMAIL2
}


USER1P = {
    "username": USERNAME1,
    "password": generate_password_hash(PASSWORD1),
    "email": EMAIL1
}

USER2P = {
    "username": USERNAME2,
    "password": generate_password_hash(PASSWORD2),
    "email": EMAIL2
}

SERIES_NAME = 'Series Name'
PAYER1 = 'Payer1'
PAYER2 = 'Payer2'
PAYEE1 = 'Payee1'
PAYEE2 = 'Payee2'
START_DATE1 = '1982-05-14'
START_DATE1_DATE = datetime.strptime(START_DATE1, '%Y-%m-%d')
START_DATE2 = '1984-05-14'
START_DATE2_DATE = datetime.strptime(START_DATE2, '%Y-%m-%d')
END_DATE1 = '1984-05-14'
END_DATE1_DATE = datetime.strptime(END_DATE1, '%Y-%m-%d')
END_DATE2 = '1986-05-14'
END_DATE2_DATE = datetime.strptime(END_DATE2, '%Y-%m-%d')
FREQUENCY = 'monthly'
AMOUNT = 123.45
ACCOUNT_NAME1 = 'ACCOUNT_NAME1'
ACCOUNT_NAME2 = 'ACCOUNT_NAME2'
ACCOUNT_OPENED_DATE1 = datetime.strptime('1982-05-14', '%Y-%m-%d')


STANDARD_SERIES1 = {
    'name': SERIES_NAME,
    'username': USERNAME1,
    'payer': PAYER1,
    'payee': PAYEE1,
    'amount': AMOUNT,
    'start_date': START_DATE1_DATE.date(),
    'end_date': END_DATE1_DATE.date(),
    'frequency': FREQUENCY
}


STANDARD_SERIES2 = {
    'name': SERIES_NAME,
    'username': USERNAME1,
    'payer': PAYER2,
    'payee': PAYEE2,
    'amount': AMOUNT,
    'start_date': START_DATE2_DATE.date(),
    'end_date': END_DATE2_DATE.date(),
    'frequency': FREQUENCY
}


STANDARD_SERIES_NO_PAYER = {
    'name': SERIES_NAME,
    'username': USERNAME1,
    'payer': '',
    'payee': PAYEE1,
    'amount': AMOUNT,
    'start_date': START_DATE1_DATE.date(),
    'end_date': END_DATE1_DATE.date(),
    'frequency': FREQUENCY
}

STANDARD_SERIES_ACCOUNT = {
    'name': SERIES_NAME,
    'username': USERNAME1,
    'payer': PAYER1,
    'payee': '',
    'payee_account': ACCOUNT_NAME1,
    'amount': AMOUNT,
    'start_date': START_DATE1_DATE.date(),
    'end_date': END_DATE1_DATE.date(),
    'frequency': FREQUENCY
}


@pytest.fixture
def app():

    app = create_app({'TESTING': True,
                      'WTF_CSRF_ENABLED': False,
                      'DEBUG': True,
                      'SECRET_KEY': 'someSecret5hizz',
                      'MONGODB_SETTINGS': {'MONGO_URI': os.environ['MONGO_URI']}
                      })
    
    with app.app_context():
        get_db()['users'].insert_one(USER1P)
        get_db()['users'].insert_one(USER2P)
    
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

    def login(self, data=None):
        if data is None:
            data = USER1
        return self._client.post(
            '/auth/login',
            data=data,
            follow_redirects=True
        )

    def logout(self):
        return self._client.get(
            '/auth/logout',
            follow_redirects=True
        )

    def register(self, data):
        return self._client.post(
            '/auth/register',
            data=data,
            follow_redirects=True
        )
        
    def post_and_redirect(self, url, data=None):
        return self._client.post(
            url, 
            data=data,
            follow_redirects=True
        )
        
    def post(self, url, data=None):
        return self._client.post(
            url, 
            data=data,
        )
        
    def get_and_redirect(self, url, data=None):
        return self._client.get(
            url, 
            data=data, 
            follow_redirects=True
        )
        
    def get(self, url, data=None):
        return self._client.get(
            url, 
            data=data,
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)


class TestUser(object):
    def __init__(self, app):
        self.app = app
        
    def get_user_id(self, username=USERNAME1):
        with self.app.app_context():
            return str(get_db()['users'].find_one({"username": username})['_id'])
            
    def get_username(self, username=USERNAME1):
        with self.app.app_context():
            return get_db()['users'].find_one({"username": username})['username']
            
    def get_user_from_username(self, username=USERNAME1):
        with self.app.app_context():
            return get_db()['user'].find_one({"username": username})
            
    def get_user_from_user_id(self, user_id):
        with self.app.app_context():
            return get_db()['user'].find_one({"username": ObjectId(user_id)})


@pytest.fixture
def test_user(app):
    return TestUser(app)


