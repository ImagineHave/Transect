from datetime import datetime
from transect.domain.transactions import insert_transaction, get_transactions_for_user_id, get_transactions
from dateutil.relativedelta import relativedelta


def create_transactions(username, payer='A', payee='B', amount=100.0, date='1982-05-14', count=1):
    transactions = []
    for i in range(count):
        dt = datetime.strptime(date, '%Y-%m-%d') + relativedelta(months=i)
        t = {'username': username, 'payer': payer, 'payee': payee, 'amount': amount, 'date_due': dt}
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
                               date_due=transaction['date_due'])

        for transaction in t2s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date_due=transaction['date_due'])

        for transaction in t1s:
            auth.post('/transactions/add', data=transaction)

        assert len(get_transactions_for_user_id(user_id1)) == 5

        for transaction in t1s:
            assert len(get_transactions({'date_due': transaction['date_due'], 'user': transaction['username']})) == 1
            assert get_transactions({
                'date_due': transaction['date_due'],
                'user': transaction['username']})[0]['date_due'] == transaction['date_due']


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
                               date_due=transaction['date_due'])

        for transaction in t2s:
            insert_transaction(username=transaction['username'],
                               payer=transaction['payer'],
                               payee=transaction['payee'],
                               amount=transaction['amount'],
                               date_due=transaction['date_due'])

        assert len(get_transactions_for_user_id(user_id1)) == 5

        d1 = {'user': username1, 'payer': 'A'}
        d2 = {'user': username2, 'payer': 'A'}
        t1id = get_transactions(d1).first().get_id()
        t2id = get_transactions(d2).first().get_id()

        t = create_transactions(username1, payee='C', date='1975-05-31')[0]

        change_logged_in_users_transaction = '/transactions/' + t1id + '/edit'
        change_non_logged_in_users_transaction = '/transactions/' + t2id + '/edit'

        response = auth.post_and_redirect(change_logged_in_users_transaction, data=t)

        assert 200 == response.status_code

        response = auth.post_and_redirect(change_non_logged_in_users_transaction, data=t)

        print(response.data)

        assert 403 == response.status_code

        assert len(get_transactions_for_user_id(user_id1)) == 5

        assert get_transactions({'user': username1, 'payee': 'C'}).count() != 0
        assert get_transactions({'user': username1, 'payee': 'C'}).first().date_due == t['date_due']
        assert get_transactions({'user': username2, 'payee': 'C'}) == []


def test_deleting_transactions(client, app, auth, test_user):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        logged_in_id = test_user.get_user_id()
        other_id = test_user.get_user_id(username='test1')

        test_transactions.create_transactions(logged_in_id, count=6)
        test_transactions.create_transactions(other_id, count=7)

        assert len(test_transactions.get_transactions_for_user_id(logged_in_id)) == 6

        t1 = {'user_id': logged_in_id, 'date': '1982-05-14'}
        t2 = {'user_id': other_id, 'date': '1982-05-14'}
        t1id = test_transactions.get_transaction_id(t1)
        t2id = test_transactions.get_transaction_id(t2)

        change_logged_in_users_transaction = '/transactions/' + t1id + '/delete'
        change_non_logged_in_users_transaction = '/transactions/' + t2id + '/delete'

        response = auth.post_and_redirect(change_logged_in_users_transaction)

        assert 200 == response.status_code

        response = auth.post_and_redirect(change_non_logged_in_users_transaction)

        print(response.data)

        assert 403 == response.status_code

        assert len(test_transactions.get_transactions_for_user_id(logged_in_id)) == 5

        for t in test_transactions.get_transactions_for_user_id(logged_in_id):
            print(t)

        assert test_transactions.get_transaction({'user_id': logged_in_id, 'date': '1982-05-14'}) == []


def test_all_transactions(client, app, auth, test_user):
    with app.app_context():
        all_transactions = '/transactions/all'
        response = auth.get_and_redirect(all_transactions)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.get_and_redirect(all_transactions)
        assert b"home" in response.data
        assert b"add" in response.data
        assert b"bulk" in response.data

        logged_in_id = test_user.get_user_id()
        other_id = test_user.get_user_id('test1')

        t1s = create_transactions(logged_in_id, count=100)
        test_transactions.create_transactions(other_id, count=2)

        for transaction in t1s:
            response = auth.post_and_redirect('/transactions/add', data=transaction)
        assert b'all' in response.data

        assert len(test_transactions.get_transactions_for_user_id(logged_in_id)) == 100
        for transaction in t1s:
            assert transaction['date'].encode() in response.data
            assert str(transaction['amount']).encode() in response.data
