from datetime import datetime
from transect.domain.transactions import insert_transaction, get_transactions_for_user_id, get_transactions
from tests.domain.test_transactions import create_transactions
from tests.conftest import (
    USERNAME1, USERNAME2, PAYER1, PAYEE1, AMOUNT, START_DATE1_DATE, PAYER2, PAYEE2, START_DATE2, START_DATE2_DATE
)


def test_home(client, auth):
    index = '/'
    response = auth.get_and_redirect(index)
    assert b"login" in response.data
    assert b"register" in response.data

    auth.login()
    response = auth.get_and_redirect(index)
    assert b'logout' in response.data
    assert b'home' in response.data


def test_adding_transactions(client, app, auth, test_user):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)

        t1s = create_transactions(count=5)

        assert 5 == len(t1s)

        for transaction in t1s:
            print(transaction)
            response = auth.post_and_redirect('/transactions/add', data=transaction)
            assert 200 == response.status_code
            assert b'all' in response.data

        assert 5 == len(get_transactions_for_user_id(user_id1))

        for transaction in t1s:
            dt = datetime.combine(transaction['date'], datetime.min.time())
            assert 1 == len(get_transactions(USERNAME1, {'date': dt}))
            assert get_transactions(USERNAME1, {'date': dt}).first().date.date() == transaction['date']


def test_adding_transactions_account(client, app, auth, test_user):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)

        t1s = create_transactions(payer='', count=5)

        for transaction in t1s:
            auth.post('/transactions/add', data=transaction)

        assert len(get_transactions_for_user_id(user_id1)) == 5
        assert len(get_transactions(USERNAME1, {'payer': 'other'})) == 5


def test_editing_transactions(client, app, auth, test_user):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)

        t1s = create_transactions(count=5)
        t2s = create_transactions(count=3)

        for transaction in t1s:
            insert_transaction(USERNAME1, transaction)

        for transaction in t2s:
            insert_transaction(USERNAME2, transaction)

        assert len(get_transactions_for_user_id(user_id1)) == 5

        data = {'payer': PAYER1}
        t1id = get_transactions(USERNAME1, data).first().get_id()
        t2id = get_transactions(USERNAME2, data).first().get_id()

        t = create_transactions(USERNAME1, payee=PAYEE2, date=START_DATE2_DATE)[0]

        change_logged_in_users_transaction = '/transactions/' + t1id + '/edit'
        change_non_logged_in_users_transaction = '/transactions/' + t2id + '/edit'

        response = auth.post_and_redirect(change_logged_in_users_transaction, data=t)

        assert 200 == response.status_code

        response = auth.post_and_redirect(change_non_logged_in_users_transaction, data=t)

        assert 403 == response.status_code

        assert len(get_transactions_for_user_id(user_id1)) == 5

        assert get_transactions(USERNAME1, {'payee': PAYEE2}).count() != 0
        assert get_transactions(USERNAME1, {'payee': PAYEE2}).first().date.date() == t['date']
        assert get_transactions(USERNAME2, {'payee': PAYEE2}).count() == 0


def test_editing_transactions_account(client, app, auth, test_user):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)

        t1s = create_transactions(count=5)
        t2s = create_transactions(count=3)

        for transaction in t1s:
            insert_transaction(USERNAME1, transaction)

        for transaction in t2s:
            insert_transaction(USERNAME2, transaction)

        assert len(get_transactions_for_user_id(user_id1)) == 5

        data = {'payer': PAYER1}
        t1id = get_transactions(USERNAME1, data).first().get_id()
        t2id = get_transactions(USERNAME2, data).first().get_id()

        t = create_transactions(USERNAME1, payee='', date=START_DATE2_DATE)[0]

        change_logged_in_users_transaction = '/transactions/' + t1id + '/edit'
        change_non_logged_in_users_transaction = '/transactions/' + t2id + '/edit'

        response = auth.post_and_redirect(change_logged_in_users_transaction, data=t)

        assert 200 == response.status_code

        response = auth.post_and_redirect(change_non_logged_in_users_transaction, data=t)

        assert 403 == response.status_code

        assert len(get_transactions_for_user_id(user_id1)) == 5

        assert get_transactions(USERNAME1, {'payee': 'other'}).count() != 0
        assert get_transactions(USERNAME1, {'payee': 'other'}).first().date.date() == t['date']
        assert get_transactions(USERNAME2, {'payee': 'other'}).count() == 0


def test_deleting_transactions(client, app, auth, test_user):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)
        user_id2 = test_user.get_user_id(USERNAME2)

        t1s = create_transactions(count=4)
        t2s = create_transactions(count=2)
        t1s = t1s + create_transactions(payee=PAYEE2)
        t2s = t2s + create_transactions(payee=PAYEE2)

        for transaction in t1s:
            insert_transaction(USERNAME1, transaction)

        for transaction in t2s:
            insert_transaction(USERNAME2, transaction)

        assert len(get_transactions_for_user_id(user_id1)) == 5

        d1 = {'payee': PAYEE2}
        d2 = {'payee': PAYEE2}
        t1id = get_transactions(USERNAME1, d1).first().get_id()
        t2id = get_transactions(USERNAME2, d2).first().get_id()

        change_logged_in_users_transaction = '/transactions/' + t1id + '/delete'
        change_non_logged_in_users_transaction = '/transactions/' + t2id + '/delete'

        response = auth.post_and_redirect(change_logged_in_users_transaction)

        assert 200 == response.status_code

        response = auth.post_and_redirect(change_non_logged_in_users_transaction)

        assert 403 == response.status_code

        assert len(get_transactions_for_user_id(user_id1)) == 4
        assert len(get_transactions_for_user_id(user_id2)) == 3

        assert get_transactions(USERNAME1, {'payee': PAYEE2}).count() == 0
        assert get_transactions(USERNAME2, {'payee': PAYEE2}).count() != 0


def test_all_transactions(client, app, auth, test_user):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)

        t1s = create_transactions(count=100)
        t2s = create_transactions(count=3)

        for transaction in t2s:
            insert_transaction(USERNAME2, transaction)

        for transaction in t1s:
            response = auth.post_and_redirect('/transactions/add', data=transaction)
        assert b'all' in response.data

        assert len(get_transactions_for_user_id(user_id1)) == 100
        for transaction in t1s:
            assert str(transaction['amount']).encode() in response.data
