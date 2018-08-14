from datetime import datetime

from dateutil.relativedelta import relativedelta


def test_home(client, auth):
    index = '/'
    response = auth.get_and_redirect(index)
    assert b"login" in response.data
    assert b"register" in response.data

    auth.login()
    response = auth.get_and_redirect(index)
    assert b'logout' in response.data
    assert b'home' in response.data


def create_transactions(user_id, payer='A', payee='B', amount=100.0, date='1982-05-14', count=1):
    transactions = []
    for i in range(count):
        dt = datetime.strptime(date, '%Y-%m-%d') + relativedelta(months=i)
        date1 = dt.strftime("%Y-%m-%d")
        t = {'user_id': user_id, 'payer': payer, 'payee': payee, 'amount': amount + (i * 10), 'date': date1}
        transactions.append(t)
    return transactions


def test_adding_transactions(client, app, auth, test_user, test_transactions):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        logged_in_id = test_user.get_user_id()
        other_id = test_user.get_user_id('test1')

        t1s = create_transactions(logged_in_id, count=3)
        test_transactions.create_transactions(other_id, count=2)

        for transaction in t1s:
            auth.post('/transactions/add', data=transaction)

        assert len(test_transactions.get_transactions_for_user_id(logged_in_id)) == 3
        for transaction in t1s:
            assert len(
                test_transactions.get_transaction({'date': transaction['date'],
                                                   'user_id': transaction['user_id']})) == 1
            assert test_transactions.get_transaction({'date': transaction['date'],
                                                      'user_id': transaction['user_id']})[0][
                       'date'] == transaction['date']


def test_editing_transactions(client, app, auth, test_user, test_transactions):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        logged_in_id = test_user.get_user_id()
        other_id = test_user.get_user_id('test1')

        test_transactions.create_transactions(logged_in_id, count=6)
        test_transactions.create_transactions(other_id, count=7)

        assert len(test_transactions.get_transactions_for_user_id(logged_in_id)) == 6

        t1 = {'user_id': logged_in_id, 'date': '1982-05-14'}
        t2 = {'user_id': other_id, 'date': '1982-05-14'}
        t1id = test_transactions.get_transaction_id(t1)
        t2id = test_transactions.get_transaction_id(t2)
        t7 = create_transactions(logged_in_id, payee='C', date='1975-05-31')[0]

        change_logged_in_users_transaction = '/transactions/' + t1id + '/edit'
        change_non_logged_in_users_transaction = '/transactions/' + t2id + '/edit'

        response = auth.post_and_redirect(change_logged_in_users_transaction, data=t7)

        assert 200 == response.status_code

        response = auth.post(change_non_logged_in_users_transaction, data=t7)

        print(response.data)

        assert 403 == response.status_code

        assert len(test_transactions.get_transactions_for_user_id(logged_in_id)) == 6

        for t in test_transactions.get_transactions_for_user_id(logged_in_id):
            print(t)

        assert test_transactions.get_transaction({'user_id': logged_in_id, 'payee': 'C'}) != []
        assert test_transactions.get_transaction({'user_id': logged_in_id, 'payee': 'C'})[0]['date'] == t7['date']
        assert test_transactions.get_transaction({'user_id': other_id, 'payee': 'C'}) == []


def test_deleting_transactions(client, app, auth, test_user, test_transactions):
    with app.app_context():
        add = '/transactions/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        logged_in_id = test_user.get_user_id()
        other_id = test_user.get_user_id('test1')

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

        response = auth.post(change_non_logged_in_users_transaction)

        print(response.data)

        assert 403 == response.status_code

        assert len(test_transactions.get_transactions_for_user_id(logged_in_id)) == 5

        for t in test_transactions.get_transactions_for_user_id(logged_in_id):
            print(t)

        assert test_transactions.get_transaction({'user_id': logged_in_id, 'date': '1982-05-14'}) == []


def test_all_transactions(client, app, auth, test_user, test_transactions):
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
