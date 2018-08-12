import pytest
from flask import g, session
from transect.db import get_db, update_transaction, getUserId, get_transactions_for_user, getTransactionId
from datetime import datetime
from dateutil.relativedelta import relativedelta

def test_home(client, auth):
    index = '/'
    response = auth.openAndFollow(index)
    assert b"login" in response.data
    assert b"register" in response.data
    
    login = '/auth/login'
    response = auth.openAndFollow(login)
    assert b"login" in response.data
    assert b"register" in response.data

    auth.login()
    response = auth.openAndFollow(index)
    assert b'logout' in response.data
    assert b'home' in response.data


def createTransactions(userid, payer='A', payee='B', amount=100.0, date='1982-05-14', count=1):
    transactions = []
    for i in range(count):
        dt = datetime.strptime(date, '%Y-%m-%d') + relativedelta(months=i-1)
        t = {'userid':userid, 'payer':payer, 'payee':payee, 'amount':amount, 'date':dt}
        transactions.append(t)
    return transactions
        
        
def test_addingTransactions(client, app, auth, testUser):
    add = '/transactions/add'
    response = auth.openAndFollow(add)
    assert b"login" in response.data
    assert b"register" in response.data
    
    auth.login()
    response = auth.openAndFollow(add) 
    
    loggedInId = testUser.getUserid()
    otherId = testUser.getUserid('test1')
    
    t1s = createTransactions(loggedInId, count=3)
    t2s = createTransactions(otherId, count=2)
    
    for transaction in t1s:
        client.post('/transactions/add', data=transaction)
       
    for transaction in t2s:
        get_db()['transactions'].insert_one(transaction)
    
    with app.app_context():
        assert get_transactions_for_user(userid=userid1).count() == 3
