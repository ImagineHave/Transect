import os
import pytest
from transect import create_app
from transect.db import get_db, init_db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bson.objectid import ObjectId


@pytest.fixture
def app():
    
    app = create_app({'TESTING': True, 'WTF_CSRF_ENABLED':False, 'DEBUG':True})
    
    with app.app_context():
        init_db()
    
    with app.app_context():
        get_db()['users'].insert_one({"username":'test',"password":generate_password_hash('test'),"email":"e@ma.il"})
        get_db()['users'].insert_one({"username":'test1',"password":generate_password_hash('test1'),"email":"e2@ma.il"})
    
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
            data = {'username':'test','password':'test'}
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
        
    def postAndFollow(self,url,data=None):
        return self._client.post(
            url, 
            data=data,
            follow_redirects=True
        )
        
    def post(self,url,data=None):
        return self._client.post(
            url, 
            data=data,
        )
        
    def getAndFollow(self,url,data=None):
        return self._client.get(
            url, 
            data=data, 
            follow_redirects=True
        )
        
    def get(self,url,data=None):
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
        
    def getUserid(self, username='test'):
        with self.app.app_context():
            return str(get_db()['users'].find_one({"username":username})['_id'])
            
    def getUsername(self, username='test'):
        with self.app.app_context():
            return get_db()['users'].find_one({"username":username})['username']
            
    def getUserFromUsername(self, username='test'):
        with self.app.app_context():
            return get_db()['user'].find_one({"username":username})
            
    def getUserFromUserid(self, userid):
        with self.app.app_context():
            return get_db()['user'].find_one({"username":ObjectId(userid)})
    
@pytest.fixture
def testUser(app):
    return TestUser(app)
    

class TestTransactions(object):
    def __init__(self, app):
        self.app = app
        
    def createTransactions(self, userid, payer='A', payee='B', amount=100.0, date='1982-05-14', count=1):
        with self.app.app_context():
            for i in range(count):
                dt = datetime.strptime(date, '%Y-%m-%d') + relativedelta(months=i)
                date = dt.strftime("%Y-%m-%d")
                t = {'userid':userid, 'payer':payer, 'payee':payee, 'amount':amount+(i*10), 'date':date}
                get_db()['transactions'].insert_one(t)
                
    def getTransactionsForUserid(self, userid):
        with self.app.app_context():
            cursor = get_db()['transactions'].find({"userid":userid})
            if cursor.count() > 0:
                return list(cursor)
            else:
                return []
          
    def getTransaction(self, transaction):
        with self.app.app_context():
            cursor = get_db()['transactions'].find(transaction)
            if cursor.count() > 0:
                return list(cursor)
            else:
                return []
             
    def getTransactionId(self, transaction):
        with self.app.app_context():
            item = get_db()['transactions'].find_one(transaction)['_id']
            if item is not None:
                return str(item)
            else:
                return ""

@pytest.fixture
def testTransactions(app):
    return TestTransactions(app)
    
