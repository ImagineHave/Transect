from datetime import datetime
from bson import ObjectId
from dateutil.relativedelta import relativedelta
from transect.domain.users import Users, get_user
from transect.db import get_db
from transect.domain.transactions import insert_transaction, get_transactions, update_transaction, delete_transaction, \
    get_transactions_for_username, get_transactions_for_user_id, get_transaction


def create_transactions(username, payer='A', payee='B', amount=100.0, date='1982-05-14', count=1):
    transactions = []
    for i in range(count):
        dt = datetime.strptime(date, '%Y-%m-%d') + relativedelta(months=i)
        t = {'username': username, 'payer': payer, 'payee': payee, 'amount': amount, 'date': dt.date()}
        transactions.append(t)
    return transactions


def test_insert_transaction(app, test_user):
    with app.app_context():
        username1 = 'test'
        username2 = 'test1'

        t1s = create_transactions(username1, count=5)
        t2s = create_transactions(username2, count=3)

        for transaction in t1s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date=transaction['date'])

        for transaction in t2s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date=transaction['date'])

        user_id1 = test_user.get_user_id(username1)
        user_id2 = test_user.get_user_id(username2)

        ts1 = get_db()['transactions'].find({"user": ObjectId(user_id1)})
        ts2 = get_db()['transactions'].find({"user": ObjectId(user_id2)})

        assert 5 == ts1.count()
        assert 3 == ts2.count()


def test_get_transactions_for_username(app, test_user):
    username1 = 'test'
    t1 = create_transactions(username1)[0]
    with app.app_context():
        insert_transaction(username=t1['username'],
                           payer=t1['payer'],
                           payee=t1['payee'],
                           amount=t1['amount'],
                           date=t1['date'])
        t2 = get_transactions_for_username(username1).first()
        assert t2 is not None
        assert t1['date'] == t2['date'].date()


def test_get_transactions(app, test_user):
    username1 = 'test'
    t1 = create_transactions(username1)[0]
    with app.app_context():
        insert_transaction(username=t1['username'],
                           payer=t1['payer'],
                           payee=t1['payee'],
                           amount=t1['amount'],
                           date=t1['date'])
        t2 = get_transactions_for_username(username1).first()
        dt = datetime.combine(t1['date'], datetime.min.time())
        t2 = get_transactions(username1, {'date': dt}).first()
        assert t2 is not None
        assert t1['date'] == t2['date'].date()


def test_update_transaction(app, test_user):
    with app.app_context():
        username1 = 'test'
        username2 = 'test1'
        user_id1 = test_user.get_user_id(username1)
        user_id2 = test_user.get_user_id(username2)

        t1s = create_transactions(username1, count=5)
        t2s = create_transactions(username2, count=3)

        for transaction in t1s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date=transaction['date'])

        for transaction in t2s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date=transaction['date'])

        ts1 = get_db()['transactions'].find({"user": ObjectId(user_id1)})
        ts2 = get_db()['transactions'].find({"user": ObjectId(user_id2)})

        assert ts1.count() == 5
        assert ts2.count() == 3

        t = get_db()['transactions'].find_one({"user": ObjectId(user_id1), 'payer': 'A'})
        tid = t['_id']

        t4 = create_transactions(username1, payer='Z', payee='X')[0]

        update_transaction(tid,
                           username=t4['username'],
                           payer=t4['payer'],
                           payee=t4['payee'],
                           amount=t4['amount'],
                           date=t4['date'])

        ts1 = get_db()['transactions'].find({"user": ObjectId(user_id1)})
        ts2 = get_db()['transactions'].find({"user": ObjectId(user_id2)})

        assert ts1.count() == 5
        assert ts2.count() == 3

        t = get_db()['transactions'].find_one({"user": ObjectId(user_id1), 'payer': 'Z'})

        assert t['payee'] == 'X'


def test_delete_transaction(app, test_user):
    with app.app_context():
        username1 = 'test'
        username2 = 'test1'
        user_id1 = ObjectId(test_user.get_user_id(username1))
        user_id2 = ObjectId(test_user.get_user_id(username2))

        t1s = create_transactions(username1, count=5)
        t2s = create_transactions(username2, count=3)

        for transaction in t1s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date=transaction['date'])

        for transaction in t2s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date=transaction['date'])

        ts1 = get_db()['transactions'].find({"user": user_id1})
        ts2 = get_db()['transactions'].find({"user": user_id2})

        assert ts1.count() == 5
        assert ts2.count() == 3

        t = get_db()['transactions'].find_one({"user": user_id1, 'payer': 'A'})
        tid = t['_id']

        delete_transaction(tid)

        ts1 = get_db()['transactions'].find({"user": user_id1})
        ts2 = get_db()['transactions'].find({"user": user_id2})

        assert ts1.count() == 4
        assert ts2.count() == 3


def test_get_transaction_id(app, test_user):
    with app.app_context():
        username1 = 'test'
        user_id1 = ObjectId(test_user.get_user_id(username1))

        ts = create_transactions(username1, count=1)

        for transaction in ts:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date=transaction['date'])

        tid = get_db()['transactions'].find_one({"user": user_id1})['_id']

        assert str(get_db()['transactions'].find_one({"_id": tid})['_id']) == str(get_transaction(
            tid).id)


def test_get_transactions_for_username(app, test_user):
    with app.app_context():
        username1 = 'test'
        username2 = 'test1'

        t1s = create_transactions(username1, count=3)
        t2s = create_transactions(username2, count=4)

        for transaction in t1s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date=transaction['date'])

        for transaction in t2s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date=transaction['date'])

        ts1 = get_transactions_for_username(username1)
        ts2 = get_transactions_for_username(username2)

        assert ts1.count() == 3
        assert ts2.count() == 4


def test_get_transactions_for_user_id(app, test_user):
    with app.app_context():
        username1 = 'test'
        username2 = 'test1'
        user_id1 = ObjectId(test_user.get_user_id(username1))
        user_id2 = ObjectId(test_user.get_user_id(username2))

        t1s = create_transactions(username1, count=3)
        t2s = create_transactions(username2, count=4)

        for transaction in t1s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date=transaction['date'])

        for transaction in t2s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date=transaction['date'])

        ts1 = get_transactions_for_user_id(user_id1)
        ts2 = get_transactions_for_user_id(user_id2)

        assert ts1.count() == 3
        assert ts2.count() == 4
