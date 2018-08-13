import pytest
from flask import g, session
from datetime import datetime
from dateutil.relativedelta import relativedelta

def test_home(client, auth):
    index = '/'
    response = auth.getAndFollow(index)
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
        t = {'userid':userid, 'payer':payer, 'payee':payee, 'amount':amount+(i*10), 'date':date}
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
            response = auth.post('/transactions/add', data=transaction)
            
        assert len(testTransactions.getTransactionsForUserid(loggedInId)) == 3
        for transaction in t1s:
            assert len(testTransactions.getTransaction({'date':transaction['date'], 'userid':transaction['userid']})) == 1
            assert testTransactions.getTransaction({'date':transaction['date'], 'userid':transaction['userid']})[0]['date'] == transaction['date']

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
        
        assert len(testTransactions.getTransactionsForUserid(loggedInId)) == 6
    
        t1 = {'userid':loggedInId,'date':'1982-05-14'}
        t2 = {'userid':otherId,'date':'1982-05-14'}
        t1id = testTransactions.getTransactionId(t1)
        t2id = testTransactions.getTransactionId(t2)
        t7 = createTransactions(loggedInId, payee='C', date='1975-05-31')[0]
    
        
        changeLoggedInUsersTransaction = '/transactions/'+t1id+'/edit'
        changeNonLoggedInUsersTransaction = '/transactions/'+t2id+'/edit'
        
        
        response = auth.postAndFollow(changeLoggedInUsersTransaction, data=t7)
        
        assert response.status_code == 200
        
        response = auth.post(changeNonLoggedInUsersTransaction, data=t7)
        
        assert response.status_code == 403
        
        assert len(testTransactions.getTransactionsForUserid(loggedInId)) == 6
        
        for t in testTransactions.getTransactionsForUserid(loggedInId):
            print(t)
        
        assert testTransactions.getTransaction({'userid':loggedInId,'payee':'C'}) != []
        assert testTransactions.getTransaction({'userid':loggedInId,'payee':'C'})[0]['date'] == t7['date']
        assert testTransactions.getTransaction({'userid':otherId,'payee':'C'}) == []
        
def test_deletingTransactions(client, app, auth, testUser, testTransactions):
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
        
        assert len(testTransactions.getTransactionsForUserid(loggedInId)) == 6
    
        t1 = {'userid':loggedInId,'date':'1982-05-14'}
        t2 = {'userid':otherId,'date':'1982-05-14'}
        t1id = testTransactions.getTransactionId(t1)
        t2id = testTransactions.getTransactionId(t2)

        
        changeLoggedInUsersTransaction = '/transactions/'+t1id+'/delete'
        changeNonLoggedInUsersTransaction = '/transactions/'+t2id+'/delete'
        
        
        response = auth.postAndFollow(changeLoggedInUsersTransaction)
        
        assert response.status_code == 200
        
        response = auth.post(changeNonLoggedInUsersTransaction)
        
        assert response.status_code == 403
        
        assert len(testTransactions.getTransactionsForUserid(loggedInId)) == 5
        
        for t in testTransactions.getTransactionsForUserid(loggedInId):
            print(t)
        
        assert testTransactions.getTransaction({'userid':loggedInId,'date':'1982-05-14'}) == []
        
def test_allTransactions(client, app, auth, testUser, testTransactions):
    with app.app_context():
        all = '/transactions/all'
        response = auth.getAndFollow(all)
        assert b"login" in response.data
        assert b"register" in response.data
        
        auth.login()
        response = auth.getAndFollow(all) 
        assert b"home" in response.data
        assert b"add" in response.data
        assert b"bulk" in response.data
        
        loggedInId = testUser.getUserid()
        otherId = testUser.getUserid('test1')
        
        t1s = createTransactions(loggedInId, count=100)
        testTransactions.createTransactions(otherId, count=2)
        
        for transaction in t1s:
            response = auth.postAndFollow('/transactions/add', data=transaction)
        assert b'all' in response.data
        
        assert len(testTransactions.getTransactionsForUserid(loggedInId)) == 100
        for transaction in t1s:
            assert transaction['date'].encode() in response.data
            assert str(transaction['amount']).encode() in response.data