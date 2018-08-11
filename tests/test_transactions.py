import pytest
from flask import g, session
from transect.db import get_db, update_transaction, getUserId, get_transactions_for_user, getTransactionId

def test_home(client, auth):
    assert client.get('/').status_code == 302
    
    response = client.get('/auth/login')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'Welcome home' in response.data
    
    
def insertSomeTransactions(app):
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
        
        
def test_addingTransactions(client, app, auth):
    assert client.get('/transactions/add').status_code == 302
    
    auth.login()
    assert client.get('/transactions/add').status_code == 200
    with app.app_context():
        user1 = get_db()['users'].find_one({'username':'test'})
        user2 = get_db()['users'].find_one({'username':'test1'})
        userid1 = getUserId(user1)
        userid2 = getUserId(user2)
        t = {'userid':userid2,'date':3,'payer':'c','amount':3,'payee':'a'}
        get_db()['transactions'].insert_one(t)
    
    date = 'date'
    payer = 'payer'
    amount = 'amount'
    payee = 'payee'
    transaction1 = {"userid":userid1, "date":date, "payer":payer, "amount":amount, "payee":payee+'1'}
    transaction2 = {"userid":userid1, "date":date, "payer":payer, "amount":amount, "payee":payee+'2'}
    
    client.post('/transactions/add', data=transaction1)
    client.post('/transactions/add', data=transaction2)
    
    with app.app_context():
        assert get_transactions_for_user(userid=userid1).count() == 2


def test_editingTransactions(client, app, auth):
    assert client.get('/transactions/add').status_code == 302
    
    auth.login()
    assert client.get('/transactions/add').status_code == 200
    with app.app_context():
        user1 = get_db()['users'].find_one({'username':'test'})
        user2 = get_db()['users'].find_one({'username':'test1'})
        
        userid1 = getUserId(user1)
        userid2 = getUserId(user2)
        
        t = {'userid':userid2,'date':3,'payer':'c','amount':3,'payee':'a'}
        get_db()['transactions'].insert_one(t)
    
    
    date = '1'
    payer = 'payer'
    amount = 'amount'
    transaction1 = {"userid":userid1, "date":date, "payer":payer, "amount":amount, "payee":'1'}
    transaction2 = {"userid":userid1, "date":date, "payer":payer, "amount":amount, "payee":'2'}
    
    client.post('/transactions/add', data=transaction1)
    client.post('/transactions/add', data=transaction2)
    
    with app.app_context():
        assert get_transactions_for_user(userid=userid1).count() == 2
        t1 = getTransactionId(get_db()['transactions'].find_one({"userid":userid1, "payee":'1'}))
        t2 = getTransactionId(get_db()['transactions'].find_one({"userid":userid1, "payee":'2'}))
        t3 = getTransactionId(get_db()['transactions'].find_one({"userid":userid2}))
        
    transaction3 = {"userid":userid1, "date":date, "payer":payer, "amount":amount, "payee":'3'}
        
    client.post('/transactions/'+t1+'/edit', data=transaction3)
    assert client.post('/transactions/'+t3+'/edit').status_code == 403
    
    with app.app_context():
        assert get_transactions_for_user(userid=userid1).count() == 2
        
def test_deletingTransactions(client, app, auth):
    assert client.get('/transactions/add').status_code == 302
    
    auth.login()
    assert client.get('/transactions/add').status_code == 200
    with app.app_context():
        user1 = get_db()['users'].find_one({'username':'test'})
        user2 = get_db()['users'].find_one({'username':'test1'})
        
        userid1 = getUserId(user1)
        userid2 = getUserId(user2)
        
        t = {'userid':userid2,'date':3,'payer':'c','amount':3,'payee':'a'}
        get_db()['transactions'].insert_one(t)
    
    
    date = 'date'
    payer = 'payer'
    amount = 'amount'
    transaction1 = {"userid":userid1, "date":date, "payer":payer, "amount":amount, "payee":'1'}
    transaction2 = {"userid":userid1, "date":date, "payer":payer, "amount":amount, "payee":'2'}
    
    client.post('/transactions/add', data=transaction1)
    client.post('/transactions/add', data=transaction2)
    
    with app.app_context():
        assert get_transactions_for_user(userid=userid1).count() == 2
        t1 = getTransactionId(get_db()['transactions'].find_one({"userid":userid1, "payee":'1'}))
        t2 = getTransactionId(get_db()['transactions'].find_one({"userid":userid1, "payee":'2'}))
        t3 = getTransactionId(get_db()['transactions'].find_one({"userid":userid2}))
        
    
    client.post('/transactions/'+t1+'/delete')
    assert client.post('/transactions/'+t3+'/delete').status_code == 403
    
    with app.app_context():
        assert get_transactions_for_user(userid=userid1).count() == 1
        assert get_transactions_for_user(userid=userid2).count() == 1
    


