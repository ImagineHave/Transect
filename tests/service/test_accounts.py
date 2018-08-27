from datetime import datetime
from transect.domain.accounts import get_accounts_by_username, get_accounts


def create_accounts(
        account_name='ACCOUNT',
        account_opened_date='1982-05-14',
        credit_or_debit=True,
        username='test',
        count=1):

    accounts = []
    for i in range(count):
        a = {
            'account_name': account_name,
            'username': username,
            'credit_or_debit': credit_or_debit,
            'account_opened_date': datetime.strptime(account_opened_date, '%Y-%m-%d').date(),
        }
        accounts.append(a)
    return accounts


def test_adding_accounts(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        username1 = 'test'

        a1s = create_accounts()
        assert 1 == len(a1s)

        for account in a1s:
            response = auth.post('/accounts/add', data=account)
            assert b"all" in response.data

        assert 1 == len(get_accounts_by_username(username1))

        for account in a1s:
            dt = datetime.combine(account['account_opened_date'], datetime.min.time())
            assert 1 == len(get_accounts(account['username'], {'account_opened_date': dt}))
            assert account['account_opened_date'] == get_accounts(account['username'],
                                                                  {'account_opened_date': dt}).first().account_opened_date.date()


def test_editing_accounts(client, app, auth, test_user):
    with app.app_context():
        add = '/accounts/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        username1 = 'test'

        a1s = create_accounts()
        assert 1 == len(a1s)

        for series in a1s:
            auth.post_and_redirect('/accounts/add', data=series)
            assert b'all' in response.data

        assert 1 == len(get_accounts_by_username(username1))

        a1 = {'payee': 'Payee'}
        a1id = get_accounts(username1, a1).first().get_id()

        change_logged_in_users_series = '/accounts/' + a1id + '/edit'

        a1s = create_accounts(account_name='ACCOUNT2')

        response = auth.post_and_redirect(change_logged_in_users_series, data=a1s[0])

        assert 200 == response.status_code

        for account in a1s:
            assert 1 == len(get_accounts(account['account_name']))
            assert account['account_name'] == get_accounts(account['account_name']).first().account_name


def test_deleting_accounts(client, app, auth, test_user):
    with app.app_context():
        add = '/accounts/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        username1 = 'test'

        a1s = create_accounts()
        assert 1 == len(a1s)

        for series in a1s:
            auth.post_and_redirect('/accounts/add', data=series)
            assert b"all" in response.data

        assert 1 == len(get_accounts_by_username(username1))

        a1 = {'payee': 'Payee'}
        a1id = get_accounts(username1, a1).first().get_id()

        change_logged_in_users_series = '/accounts/' + a1id + '/delete'

        response = auth.post_and_redirect(change_logged_in_users_series)

        assert 200 == response.status_code

        for account in a1s:
            assert 0 == len(get_accounts(account['account_name']))
