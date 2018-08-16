from datetime import datetime

from dateutil.relativedelta import relativedelta

from transect.db import get_db
from transect.domain.transactions import insert_transaction, get_transaction, update_transaction, delete_transaction, \
    get_transactions_for_username, get_transactions_for_user_id, get_transaction_id
from transect.domain.users import get_user_id


def create_transactions(user_id, payer='A', payee='B', amount=100.0, date='1982-05-14', count=1):
    transactions = []
    for i in range(count):
        dt = datetime.strptime(date, '%Y-%m-%d') + relativedelta(months=i)
        t = {'user_id': user_id, 'payer': payer, 'payee': payee, 'amount': amount, 'date': dt}
        transactions.append(t)
    return transactions


def test_insert_transaction(app, test_user):
    with app.app_context():
        username1 = 'test'
        username2 = 'test1'
        user_id1 = test_user.get_user_id(username1)
        user_id2 = test_user.get_user_id(username2)

        t1s = create_transactions(user_id1, count=5)
        t2s = create_transactions(user_id2, count=3)

        for transaction in t1s:
            insert_transaction(transaction)

        for transaction in t2s:
            insert_transaction(transaction)

        ts1 = get_db()['transactions'].find({"user_id": user_id1})
        ts2 = get_db()['transactions'].find({"user_id": user_id2})

        assert ts1.count() == 5
        assert ts2.count() == 3


def test_get_transaction(app, test_user):
    username1 = 'test'
    user_id1 = test_user.get_user_id(username1)
    t1 = create_transactions(user_id1)[0]
    with app.app_context():
        insert_transaction(t1)
        t2 = get_transaction(t1)
        assert t2 is not None
        assert t1['date'] == t2['date']


def test_update_transaction(app, test_user, test_transactions):
    with app.app_context():
        username1 = 'test'
        username2 = 'test1'
        user_id1 = test_user.get_user_id(username1)
        user_id2 = test_user.get_user_id(username2)

        t1s = create_transactions(user_id1, count=5)
        t2s = create_transactions(user_id2, count=3)

        for transaction in t1s:
            insert_transaction(transaction)

        for transaction in t2s:
            insert_transaction(transaction)

        ts1 = get_db()['transactions'].find({"user_id": user_id1})
        ts2 = get_db()['transactions'].find({"user_id": user_id2})

        assert ts1.count() == 5
        assert ts2.count() == 3

        t = get_db()['transactions'].find_one({"user_id": user_id1, 'payer': 'A'})
        tid = t['_id']

        t4 = create_transactions(user_id1, payer='Z', payee='X')[0]

        update_transaction(tid, t4)

        ts1 = get_db()['transactions'].find({"user_id": user_id1})
        ts2 = get_db()['transactions'].find({"user_id": user_id2})

        assert ts1.count() == 5
        assert ts2.count() == 3

        t = get_db()['transactions'].find_one({"user_id": user_id1, 'payer': 'Z'})

        assert t['payee'] == 'X'


def test_delete_transaction(app, test_user, test_transactions):
    with app.app_context():
        username1 = 'test'
        username2 = 'test1'
        user_id1 = test_user.get_user_id(username1)
        user_id2 = test_user.get_user_id(username2)

        t1s = create_transactions(user_id1, count=5)
        t2s = create_transactions(user_id2, count=3)

        for transaction in t1s:
            insert_transaction(transaction)

        for transaction in t2s:
            insert_transaction(transaction)

        ts1 = get_db()['transactions'].find({"user_id": user_id1})
        ts2 = get_db()['transactions'].find({"user_id": user_id2})

        assert ts1.count() == 5
        assert ts2.count() == 3

        t = get_db()['transactions'].find_one({"user_id": user_id1, 'payer': 'A'})
        tid = t['_id']

        delete_transaction(tid)

        ts1 = get_db()['transactions'].find({"user_id": user_id1})
        ts2 = get_db()['transactions'].find({"user_id": user_id2})

        assert ts1.count() == 4
        assert ts2.count() == 3


def test_get_transaction_id(app):
    with app.app_context():
        user1 = get_db()['users'].find_one({'username': 'test'})
        user_id1 = get_user_id(user1)
        t1 = {'user_id': user_id1, 'date': 1, 'payer': 'a', 'amount': 5, 'payee': 'c'}
        get_db()['transactions'].insert_one(t1)
        tid = get_db()['transactions'].find_one({"user_id": user_id1, 'payer': 'a'})['_id']

        assert str(get_db()['transactions'].find_one({"user_id": user_id1, 'payer': 'a'})['_id']) == get_transaction_id(
            tid)


def test_get_transactions_for_username(app, test_user, test_transactions):
    with app.app_context():
        username1 = 'test'
        username2 = 'test1'
        user_id1 = test_user.get_user_id(username1)
        user_id2 = test_user.get_user_id(username2)

        test_transactions.create_transactions(user_id1, count=3)
        test_transactions.create_transactions(user_id2, count=4)

        ts1 = get_transactions_for_username(username1)
        ts2 = get_transactions_for_username(username2)

        assert ts1.count() == 3
        assert ts2.count() == 4


def test_get_transactions_for_user_id(app, test_user, test_transactions):
    with app.app_context():
        username1 = 'test'
        username2 = 'test1'
        user_id1 = test_user.get_user_id(username1)
        user_id2 = test_user.get_user_id(username2)

        test_transactions.create_transactions(user_id1, count=3)
        test_transactions.create_transactions(user_id2, count=4)

        ts1 = get_transactions_for_user_id(user_id1)
        ts2 = get_transactions_for_user_id(user_id2)

        assert ts1.count() == 3
        assert ts2.count() == 4
