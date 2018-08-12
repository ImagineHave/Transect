import pytest
from flask import g, session
from transect.db import get_db, updateTransaction, getUserId, getTransactionsForUsername, getTransactionsForUserid, getTransactionId, getTransaction
from datetime import datetime
from dateutil.relativedelta import relativedelta

def test_home(client, auth):
    index = '/'
    response = auth.getAndFollow(index)
    
    #response = client.post('/', follow_redirects=True)
    
    assert b"login" in response.data
    assert b"register" in response.data
    
    login = '/auth/login'
    response = auth.postAndFollow(login)
    assert b"login" in response.data
    assert b"register" in response.data

    auth.login()
    response = auth.getAndFollow(index)
    assert b'logout' in response.data
    assert b'home' in response.data


def createTransactions(userid, payer='A', payee='B', amount=100.0, date='1982-05-14', count=1):
    transactions = []
    for i in range(count):
        dt = datetime.strptime(date, '%Y-%m-%d') + relativedelta(months=i)
        date = dt.strftime("%Y-%m-%d")
        t = {'userid':userid, 'payer':payer, 'payee':payee, 'amount':amount, 'date':date}
        transactions.append(t)
    return transactions
        
        
def test_addingTransactions(client, app, auth, testUser, testTransactions):
    with app.app_context():
        add = '/transactions/add'
        response = auth.postAndFollow(add)
        assert b"login" in response.data
        assert b"register" in response.data
        
        auth.login()
        response = auth.postAndFollow(add) 
        assert b"add" in response.data
        
        loggedInId = testUser.getUserid()
        otherId = testUser.getUserid('test1')
        
        t1s = createTransactions(loggedInId, count=3)
        testTransactions.createTransactions(otherId, count=2)
        
        for transaction in t1s:
            response = client.post('/transactions/add', data=transaction)
            
        assert b'all' in response.data
        assert getTransactionsForUserid(loggedInId).count() == 3
        for transaction in t1s:
            assert getTransaction({'date':transaction['date'], 'userid':transaction['userid']}) is not None
            assert getTransaction({'date':transaction['date'], 'userid':transaction['userid']})['date'] == transaction['date']

def test_editingTransactions(client, app, auth, testUser, testTransactions):
    with app.app_context():
        add = '/transactions/add'
        response = auth.postAndFollow(add)
        assert b"login" in response.data
        assert b"register" in response.data
        
        auth.login()
        response = auth.postAndFollow(add) 
        assert b"add" in response.data
        
        loggedInId = testUser.getUserid()
        otherId = testUser.getUserid('test1')
        
        testTransactions.createTransactions(loggedInId, count=6)
        testTransactions.createTransactions(otherId, count=7)
        
        assert getTransactionsForUserid(loggedInId).count() == 6
    
        t1 = getTransaction({'userid':loggedInId,'date':'1982-05-14'})
        t2 = getTransaction({'userid':otherId,'date':'1982-05-14'})
        t1id = getTransactionId(t1)
        t2id = getTransactionId(t2)
        t7 = createTransactions(loggedInId, payee='C', date='1975-05-31')[0]
    
        
        changeLoggedInUsersTransaction = '/transactions/'+t1id+'/edit'
        changeNonLoggedInUsersTransaction = '/transactions/'+t2id+'/edit'
        
        response = client.post(changeLoggedInUsersTransaction, data=t7)
        response = client.post(changeNonLoggedInUsersTransaction, data=t7)
        
        assert response.status_code == 403
        
        assert getTransactionsForUserid(loggedInId).count() == 6
        assert getTransaction({'userid':loggedInId,'payee':'C'})['date'] == t7['date']
        assert getTransaction({'userid':otherId,'payee':'C'})['date'] is None