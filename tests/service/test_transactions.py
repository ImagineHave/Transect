from datetime import datetime
from transect.domain.transactions import insert_transaction, get_transactions_for_user_id, get_transactions
from dateutil.relativedelta import relativedelta


def create_transactions(username, payer='A', payee='B', amount=100.0, date='1982-05-14', count=1):
    transactions = []
    for i in range(count):
        dt = datetime.strptime(date, '%Y-%m-%d') + relativedelta(months=i)
        t = {'username': username, 'payer': payer, 'payee': payee, 'amount': amount, 'date': dt.date()}
        transactions.append(t)
    return transactions


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

        username1 = 'test'
        user_id1 = test_user.get_user_id(username1)

        t1s = create_transactions(username1, count=5)

        for transaction in t1s:
            auth.post('/transactions/add', data=transaction)

        assert len(get_transactions_for_user_id(user_id1)) == 5

        for transaction in t1s:
            print(transaction)
            dt = datetime.combine(transaction['date'], datetime.min.time())
            assert len(get_transactions(transaction['username'], {'date_due': dt})) == 1
            assert get_transactions(transaction['username'], {'date_due': dt}).first().date_due.date() == transaction['date']


def test_editing_transactions(client, app, auth, test_user):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

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
                               date_due=transaction['date'])

        for transaction in t2s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date_due=transaction['date'])

        assert len(get_transactions_for_user_id(user_id1)) == 5

        d1 = {'payer': 'A'}
        d2 = {'payer': 'A'}
        t1id = get_transactions(username1, d1).first().get_id()
        t2id = get_transactions(username2, d2).first().get_id()

        t = create_transactions(username1, payee='C', date='1975-05-31')[0]

        change_logged_in_users_transaction = '/transactions/' + t1id + '/edit'
        change_non_logged_in_users_transaction = '/transactions/' + t2id + '/edit'

        response = auth.post_and_redirect(change_logged_in_users_transaction, data=t)

        assert 200 == response.status_code

        response = auth.post_and_redirect(change_non_logged_in_users_transaction, data=t)

        assert 403 == response.status_code

        assert len(get_transactions_for_user_id(user_id1)) == 5

        assert get_transactions(username1, {'payee': 'C'}).count() != 0
        assert get_transactions(username1, {'payee': 'C'}).first().date_due.date() == t['date']
        assert get_transactions(username2, {'payee': 'C'}).count() == 0


def test_deleting_transactions(client, app, auth, test_user):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        username1 = 'test'
        username2 = 'test1'
        user_id1 = test_user.get_user_id(username1)
        user_id2 = test_user.get_user_id(username2)

        t1s = create_transactions(username1, count=4)
        t2s = create_transactions(username2, count=2)
        t1s = t1s + create_transactions(username1, payee='C')
        t2s = t2s + create_transactions(username2, payee='C')

        for transaction in t1s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date_due=transaction['date'])

        for transaction in t2s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date_due=transaction['date'])

        assert len(get_transactions_for_user_id(user_id1)) == 5

        d1 = {'payee': 'C'}
        d2 = {'payee': 'C'}
        t1id = get_transactions(username1, d1).first().get_id()
        t2id = get_transactions(username2, d2).first().get_id()

        change_logged_in_users_transaction = '/transactions/' + t1id + '/delete'
        change_non_logged_in_users_transaction = '/transactions/' + t2id + '/delete'

        response = auth.post_and_redirect(change_logged_in_users_transaction)

        assert 200 == response.status_code

        response = auth.post_and_redirect(change_non_logged_in_users_transaction)

        assert 403 == response.status_code

        assert len(get_transactions_for_user_id(user_id1)) == 4
        assert len(get_transactions_for_user_id(user_id2)) == 3

        assert get_transactions(username1, {'payee': 'C'}).count() == 0
        assert get_transactions(username2, {'payee': 'C'}).count() != 0


def test_all_transactions(client, app, auth, test_user):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        username1 = 'test'
        username2 = 'test1'
        user_id1 = test_user.get_user_id(username1)

        t1s = create_transactions(username1, count=100)
        t2s = create_transactions(username2, count=3)

        for transaction in t2s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date_due=transaction['date'])

        for transaction in t1s:
            response = auth.post_and_redirect('/transactions/add', data=transaction)
        assert b'all' in response.data

        assert len(get_transactions_for_user_id(user_id1)) == 100
        for transaction in t1s:
            assert str(transaction['amount']).encode() in response.data
