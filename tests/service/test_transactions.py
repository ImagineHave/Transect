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

        t1s = create_transactions(payer='Payer3', payee='Payee3')

        assert 1 == len(t1s)

        for transaction in t1s:
            print(transaction)
            response = auth.post_and_redirect('/transactions/add', data=transaction)
            assert 200 == response.status_code
            assert b'all' in response.data

        assert 1 == len(get_transactions_for_user_id(user_id1))

        for transaction in t1s:
            dt = datetime.combine(transaction['date'], datetime.min.time())
            assert 1 == len(get_transactions({'username': USERNAME1, 'date': dt}))
            assert get_transactions({'username': USERNAME1, 'date': dt}).first().date.date() == transaction['date']


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

        t1s = create_transactions(payer='', payee='', count=5)

        for transaction in t1s:
            auth.post('/transactions/add', data=transaction)

        assert len(get_transactions_for_user_id(user_id1)) == 5
        assert len(get_transactions({'username': USERNAME1, 'payer': 'other'})) == 5


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

        t1s = create_transactions()
        t2s = create_transactions(username=USERNAME2, payee='other', payer='other', count=3)

        for transaction in t1s:
            insert_transaction(transaction)

        for transaction in t2s:
            insert_transaction(transaction)

        assert 1 == len(get_transactions_for_user_id(user_id1))

        data1 = {'username': USERNAME1, 'payer': PAYER1}
        data2 = {'username': USERNAME2, 'payer': 'other'}
        t1id = get_transactions(data1).first().get_id()
        t2id = get_transactions(data2).first().get_id()

        t = create_transactions(USERNAME1, payer='', payee='Payee3', date=START_DATE2_DATE)[0]

        change_logged_in_users_transaction = '/transactions/' + t1id + '/edit'
        change_non_logged_in_users_transaction = '/transactions/' + t2id + '/edit'

        response = auth.post_and_redirect(change_logged_in_users_transaction, data=t)

        assert 200 == response.status_code

        response = auth.post_and_redirect(change_non_logged_in_users_transaction, data=t)

        assert 403 == response.status_code

        assert 1 == len(get_transactions_for_user_id(user_id1))

        assert 0 != get_transactions({'username': USERNAME1, 'payee': 'Payee3'}).count()
        assert t['date'] == get_transactions({'username': USERNAME1, 'payee': 'Payee3'}).first().date.date()
        assert 0 == get_transactions({'username': USERNAME2, 'payee': 'Payee3'}).count()


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

        t1s = create_transactions(payee='other', payer='other', count=5)
        t2s = create_transactions(username=USERNAME2, payee='other', payer='other', count=3)

        for transaction in t1s:
            insert_transaction(transaction)

        for transaction in t2s:
            insert_transaction(transaction)

        assert len(get_transactions_for_user_id(user_id1)) == 5

        data1 = {'username': USERNAME1, 'payer': 'other'}
        data2 = {'username': USERNAME2, 'payer': 'other'}
        t1id = get_transactions(data1).first().get_id()
        t2id = get_transactions(data2).first().get_id()

        t = create_transactions(USERNAME1, payer='', payee='', date=START_DATE2_DATE)[0]
        t['payee_account'] = PAYEE1
        t['payer_account'] = 'other'

        change_logged_in_users_transaction = '/transactions/' + t1id + '/edit'
        change_non_logged_in_users_transaction = '/transactions/' + t2id + '/edit'

        response = auth.post_and_redirect(change_logged_in_users_transaction, data=t)

        assert 200 == response.status_code

        response = auth.post_and_redirect(change_non_logged_in_users_transaction, data=t)

        assert 403 == response.status_code

        assert len(get_transactions_for_user_id(user_id1)) == 5

        assert get_transactions({'username': USERNAME1, 'payee': PAYEE1}).count() != 0
        assert get_transactions({'username': USERNAME1, 'payee': PAYEE1}).first().date.date() == t['date']
        assert get_transactions({'username': USERNAME2, 'payee': PAYEE1}).count() == 0


def test_deleting_transactions(client, app, auth, test_user):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        t1s = create_transactions(count=4)
        t2s = create_transactions(username=USERNAME2, count=2)
        t1s = t1s + create_transactions(payee=PAYEE2)
        t2s = t2s + create_transactions(username=USERNAME2, payee=PAYEE2)

        for transaction in t1s:
            insert_transaction(transaction)

        for transaction in t2s:
            insert_transaction(transaction)

        assert 5 == len(get_transactions({'username': USERNAME1}))

        d1 = {'username': USERNAME1, 'payee': PAYEE2}
        d2 = {'username': USERNAME2, 'payee': PAYEE2}
        t1id = get_transactions(d1).first().get_id()
        t2id = get_transactions(d2).first().get_id()

        change_logged_in_users_transaction = '/transactions/' + t1id + '/delete'
        change_non_logged_in_users_transaction = '/transactions/' + t2id + '/delete'

        response = auth.post_and_redirect(change_logged_in_users_transaction)

        assert 200 == response.status_code

        response = auth.post_and_redirect(change_non_logged_in_users_transaction)

        assert 403 == response.status_code

        assert 4 == len(get_transactions({'username': USERNAME1}))
        assert 3 == len(get_transactions({'username': USERNAME2}))

        assert get_transactions({'username': USERNAME1, 'payee': PAYEE2}).count() == 0
        assert get_transactions({'username': USERNAME2, 'payee': PAYEE2}).count() != 0


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

        t1s = create_transactions(payer=PAYER1, payee=PAYEE1, count=100)
        t2s = create_transactions(payer=PAYER1, payee=PAYEE1, username=USERNAME2, count=3)

        for transaction in t2s:
            insert_transaction(transaction)

        for transaction in t1s:
            response = auth.post_and_redirect('/transactions/add', data=transaction)
        assert b'all' in response.data

        assert len(get_transactions_for_user_id(user_id1)) == 100
        for transaction in t1s:
            assert str(transaction['amount']).encode() in response.data
