from transect.db import (
    get_db, create_user, get_by_username, get_by_user_id, get_user, get_username_from_user_id,
    get_user_id_from_username, does_password_match_user, get_user_id, get_transactions_for_username,
    get_transactions_for_user_id, insert_transaction, update_transaction, delete_transaction, get_transaction_id,
    does_username_exist, validate_user_password, get_transaction
)
from datetime import datetime
from dateutil.relativedelta import relativedelta


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()


def test_set_user(app):
    with app.app_context():
        create_user('a', 'a', 'a')
        assert get_db()['users'].find_one({'username': 'a'}) is not None


def test_get_by_username(app):
    with app.app_context():
        assert get_by_username('test') is not None


def test_get_by_user_id(app):
    with app.app_context():
        user = get_db()['users'].find_one({'username': 'test'})
        get_by_user_id(str(user['_id']))


def test_get_user(app):
    with app.app_context():
        user = get_db()['users'].find_one({'username': 'test'})
        user_id = str(user['_id'])
        assert get_user(username='test') == user
        assert get_user(_id=user_id) == user
        assert get_user(_id=None, username='test') == user
        assert get_user(username=None, _id=user_id) == user
        assert get_user(username='test', _id=user_id) == user
        assert get_user(_id=None, username=None) is None


def test_get_username_from_id(app, test_user):
    with app.app_context():
        user_id = test_user.get_user_id()
        assert get_username_from_user_id(user_id) == test_user.get_username()
        notid = test_user.get_user_id()
        notid = notid[-1:] + notid[1:-1] + notid[:1]
        assert get_username_from_user_id(notid) is not test_user.get_username()
        assert get_username_from_user_id(None) is not test_user.get_username()


def test_get_user_id_from_username(app, test_user):
    with app.app_context():
        assert get_user_id_from_username('test') == test_user.get_user_id()
        assert get_user_id_from_username('test1') is not test_user.get_user_id()
        assert get_user_id_from_username(None) is not test_user.get_user_id()


def test_check_password_for_user(app):
    with app.app_context():
        assert does_password_match_user('test', 'test')
        assert does_password_match_user('test') is None
        assert does_password_match_user('test', 'notpasswrd') is False


def test_get_user_id(app):
    with app.app_context():
        user = get_db()['users'].find_one({'username': 'test'})
        user_id = str(user['_id'])
        assert user_id == get_user_id(user)


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


def test_does_username_exist(app):
    with app.app_context():
        assert does_username_exist('test')
        assert not does_username_exist('as98fsd987045h0hd89f98h45b')
        assert not does_username_exist(None)


def test_validate_user_password(app):
    with app.app_context():
        assert validate_user_password('test', 'test')
        assert not validate_user_password('test', 'somethingelse')
        assert not validate_user_password('test', None)
        assert not validate_user_password(None, 'test')


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
