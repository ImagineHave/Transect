import pytest
import pymongo
from werkzeug.security import check_password_hash, generate_password_hash
from transect.db import (
    get_db, set_user, getByUsername, getByUserId, get_user, get_username, get_userid, doesPasswordMatchUser, getUserId, get_transactions_for_user, insert_transaction,
    update_transaction, delete_transaction, getTransactionId, doesUsernameExist, validateUserPassword
    )

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
        

def test_set_user(app):
    with app.app_context():
        set_user('a','a')
        assert get_db()['users'].find_one({'username':'a'}) is not None
        

def test_getByUsername(app):
    with app.app_context():
        assert getByUsername('test') is not None
        
        
def test_getByUserId(app):
    with app.app_context():
        user = get_db()['users'].find_one({'username':'test'})
        getByUserId(str(user['_id']))


def test_get_user(app):
    with app.app_context():
        user = get_db()['users'].find_one({'username':'test'})
        userid = str(user['_id'])
        assert get_user(username='test') == user
        assert get_user(id=userid) == user
        assert get_user(id=None,username='test') == user
        assert get_user(username=None,id=userid) == user
        assert get_user(username='test',id=userid) == user
        assert get_user(id=None,username=None) is None
    
def test_get_username(app):
    with app.app_context():
        user = get_db()['users'].find_one({'username':'test'})
        userid = str(user['_id'])
        assert get_username(username='test') == 'test'
        assert get_username(id=userid) == 'test'
        assert get_username(id=None,username='test') == 'test'
        assert get_username(username=None,id=userid) == 'test'
        assert get_username(username='test',id=userid) == 'test'
        assert get_username(id=None,username=None) is None
        
def test_get_userid(app):
    with app.app_context():
        user = get_db()['users'].find_one({'username':'test'})
        userid = str(user['_id'])
        assert get_userid(username='test') == userid
        assert get_userid(id=userid) == userid
        assert get_userid(id=None,username='test') == userid
        assert get_userid(username=None,id=userid) == userid
        assert get_userid(username='test',id=userid) == userid
        assert get_userid(id=None,username=None) is None
        
def test_check_password_for_user(app):
    with app.app_context():
        assert doesPasswordMatchUser('test','test')
        assert doesPasswordMatchUser('test') is None
        assert doesPasswordMatchUser('test','notpasswrd') is False
        
def test_getUserId(app):
    with app.app_context():
        user = get_db()['users'].find_one({'username':'test'})
        userid = str(user['_id'])
        assert userid == getUserId(user)
        
def test_get_transactions_for_user(app):
    with app.app_context():
        user1 = get_db()['users'].find_one({'username':'test'})
        user2 = get_db()['users'].find_one({'username':'test1'})
        
        username1 = user1['username']
        username2 = user2['username']
        
        userid1 = str(user1['_id'])
        userid2 = str(user2['_id'])
        
        t1 = {'userid':userid1,'date':1,'payer':'a','amount':5,'payee':'c'}
        t2 = {'userid':userid1,'date':2,'payer':'b','amount':4,'payee':'b'}
        t3 = {'userid':userid2,'date':3,'payer':'c','amount':3,'payee':'a'}
        
        get_db()['transactions'].insert_one(t1)
        get_db()['transactions'].insert_one(t2)
        get_db()['transactions'].insert_one(t3)
        
        ts1 = get_transactions_for_user(username1)
        ts2 = get_transactions_for_user(username2)
        
        assert ts1.count() == 2
        assert ts2.count() == 1
        
def test_insert_transaction(app):
    with app.app_context():
        user1 = get_db()['users'].find_one({'username':'test'})
        user2 = get_db()['users'].find_one({'username':'test1'})
        
        userid1 = str(user1['_id'])
        userid2 = str(user2['_id'])
        
        t1 = {'userid':userid1,'date':1,'payer':'a','amount':5,'payee':'c'}
        t2 = {'userid':userid1,'date':2,'payer':'b','amount':4,'payee':'b'}
        t3 = {'userid':userid2,'date':3,'payer':'c','amount':3,'payee':'a'}
        
        insert_transaction(t1)
        insert_transaction(t2)
        insert_transaction(t3)
        
        ts1 = get_db()['transactions'].find({"userid":userid1})
        ts2 = get_db()['transactions'].find({"userid":userid2})
        
        assert ts1.count() == 2
        assert ts2.count() == 1        
        
def test_update_transaction(app):
    with app.app_context():
        user1 = get_db()['users'].find_one({'username':'test'})
        user2 = get_db()['users'].find_one({'username':'test1'})
        
        userid1 = str(user1['_id'])
        userid2 = str(user2['_id'])
        
        t1 = {'userid':userid1,'date':1,'payer':'a','amount':5,'payee':'c'}
        t2 = {'userid':userid1,'date':2,'payer':'b','amount':4,'payee':'b'}
        t3 = {'userid':userid2,'date':3,'payer':'c','amount':3,'payee':'a'}
        
        get_db()['transactions'].insert_one(t1)
        get_db()['transactions'].insert_one(t2)
        get_db()['transactions'].insert_one(t3)
        
        t = get_db()['transactions'].find_one({"userid":userid1,'payer':'a'})
        tid = t['_id']

        t4 = {'userid':userid1,'date':100,'payer':'z','amount':300,'payee':'x'}  
        
        update_transaction(tid,t4)
        
        ts1 = get_db()['transactions'].find({"userid":userid1})
        ts2 = get_db()['transactions'].find({"userid":userid2})
        
        assert ts1.count() == 2
        assert ts2.count() == 1    
        
        t = get_db()['transactions'].find_one({"userid":userid1,'payer':'z'})
        
        assert t['payee'] == 'x'
        

def test_delete_transaction(app):
    with app.app_context():
        user1 = get_db()['users'].find_one({'username':'test'})
        user2 = get_db()['users'].find_one({'username':'test1'})
        
        userid1 = str(user1['_id'])
        userid2 = str(user2['_id'])
        
        t1 = {'userid':userid1,'date':1,'payer':'a','amount':5,'payee':'c'}
        t2 = {'userid':userid1,'date':2,'payer':'b','amount':4,'payee':'b'}
        t3 = {'userid':userid2,'date':3,'payer':'c','amount':3,'payee':'a'}
        
        get_db()['transactions'].insert_one(t1)
        get_db()['transactions'].insert_one(t2)
        get_db()['transactions'].insert_one(t3)
        
        
        tid = get_db()['transactions'].find_one({"userid":userid1,'payer':'a'})['_id']
        
        delete_transaction(tid)
        
        ts1 = get_db()['transactions'].find({"userid":userid1})
        ts2 = get_db()['transactions'].find({"userid":userid2})
        
        assert ts1.count() == 1
        assert ts2.count() == 1  
        
        
def test_getTransactionId(app):
    with app.app_context():
        user1 = get_db()['users'].find_one({'username':'test'})
        userid1 = getUserId(user1)
        t1 = {'userid':userid1,'date':1,'payer':'a','amount':5,'payee':'c'}
        get_db()['transactions'].insert_one(t1)
        tid = get_db()['transactions'].find_one({"userid":userid1,'payer':'a'})['_id']
        
        assert str(get_db()['transactions'].find_one({"userid":userid1,'payer':'a'})['_id']) == getTransactionId(tid)
        
        
def test_doesUsernameExist(app):
    with app.app_context():
        assert doesUsernameExist('test')
        assert not doesUsernameExist('as98fsd987045h0hd89f98h45b')
        assert not doesUsernameExist(None)
        
def test_validateUserPassword(app):
    with app.app_context():
        assert validateUserPassword('test','test')
        assert not validateUserPassword('test','somethingelse')
        assert not validateUserPassword('test', None)
        assert not validateUserPassword(None,'test')