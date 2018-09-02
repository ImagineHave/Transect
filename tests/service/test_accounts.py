from datetime import datetime
from transect.domain.accounts import get_accounts_by_username, get_accounts
from transect.domain.series import get_series_by_username, get_series
from transect.domain.transactions import get_transactions_for_user_id, get_transactions
from tests.conftest import (
    USERNAME1, ACCOUNT_NAME1, ACCOUNT_OPENED_DATE1, PAYER1, ACCOUNT_NAME2, SERIES_NAME, AMOUNT,
    START_DATE1_DATE, END_DATE1_DATE, FREQUENCY, PAYEE1, STANDARD_SERIES1, STANDARD_SERIES_ACCOUNT
)


def create_accounts(
        account_name=ACCOUNT_NAME1,
        account_opened_date=ACCOUNT_OPENED_DATE1,
        count=1):

    accounts = []
    for i in range(count):
        a = {
            'account_name': account_name,
            'account_opened_date': account_opened_date.date(),
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

        user_id1 = test_user.get_user_id(USERNAME1)

        a1s = create_accounts()
        assert 1 == len(a1s)

        for account in a1s:
            response = auth.post('/accounts/add', data=account)
            assert b"all" in response.data

        assert 1 == len(get_accounts_by_username(USERNAME1))

        for account in a1s:
            date = datetime.combine(account['account_opened_date'], datetime.min.time())
            accounts = get_accounts(USERNAME1, {'account_opened_date': date})
            assert 1 == len(accounts)
            assert account['account_opened_date'] == accounts.first().account_opened_date.date()

        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        response = auth.post_and_redirect('/series/add', data=STANDARD_SERIES1)
        assert b"all" in response.data

        assert 1 == len(get_series_by_username(USERNAME1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        s1 = {'payee': PAYEE1}
        s1id = get_series(USERNAME1, s1).first().get_id()

        change_logged_in_users_series = '/series/' + s1id + '/edit'

        response = auth.post_and_redirect(change_logged_in_users_series, data=STANDARD_SERIES_ACCOUNT)

        print(response.data)

        assert 200 == response.status_code
        assert 1 == len(get_series_by_username(USERNAME1))
        date = datetime.combine(START_DATE1_DATE, datetime.min.time())
        assert 1 == len(get_transactions(USERNAME1, {'date': date}))
        assert START_DATE1_DATE == get_transactions(USERNAME1, {'date': date}).first().date
        assert ACCOUNT_NAME1 == get_transactions(USERNAME1, {'payee': ACCOUNT_NAME1}).first().payee


def test_editing_accounts(client, app, auth, test_user):
    with app.app_context():
        add = '/accounts/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        a1s = create_accounts()
        assert 1 == len(a1s)

        for account in a1s:
            response = auth.post_and_redirect('/accounts/add', data=account)
            assert b'all' in response.data

        assert 1 == len(get_accounts_by_username(USERNAME1))

        a1 = {'account_name': 'ACCOUNT_NAME1'}
        a1id = get_accounts(USERNAME1, a1).first().get_id()

        change_logged_in_users_series = '/accounts/' + a1id + '/edit'

        a1 = {'account_name': ACCOUNT_NAME2}
        a1s = create_accounts(**a1)

        response = auth.post_and_redirect(change_logged_in_users_series, data=a1s[0])

        assert 200 == response.status_code

        assert 1 == len(get_accounts(USERNAME1, a1))
        assert ACCOUNT_NAME2 == get_accounts(USERNAME1, a1).first().account_name


def test_deleting_accounts(client, app, auth, test_user):
    with app.app_context():
        add = '/accounts/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        a1s = create_accounts()
        assert 1 == len(a1s)

        for account in a1s:
            response = auth.post_and_redirect('/accounts/add', data=account)
            assert b"all" in response.data

        assert 1 == len(get_accounts_by_username(USERNAME1))

        a1 = {'account_name': 'ACCOUNT_NAME1'}
        a1id = get_accounts(USERNAME1, a1).first().get_id()

        change_logged_in_users_series = '/accounts/' + a1id + '/delete'

        response = auth.post_and_redirect(change_logged_in_users_series)

        assert 200 == response.status_code

        for account in a1s:
            assert 0 == len(get_accounts(account['account_name'], a1))


def test_add_edit_accounts(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)

        a1s = create_accounts()
        assert 1 == len(a1s)

        for account in a1s:
            response = auth.post('/accounts/add', data=account)
            assert b"all" in response.data

        assert 1 == len(get_accounts_by_username(USERNAME1))

        for account in a1s:
            date = datetime.combine(account['account_opened_date'], datetime.min.time())
            accounts = get_accounts(USERNAME1, {'account_opened_date': date})
            assert 1 == len(accounts)
            assert account['account_opened_date'] == accounts.first().account_opened_date.date()

        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        response = auth.post_and_redirect('/series/add', data=STANDARD_SERIES1)
        assert b"all" in response.data

        assert 1 == len(get_series_by_username(USERNAME1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        s1 = {'payee': PAYEE1}
        s1id = get_series(USERNAME1, s1).first().get_id()

        change_logged_in_users_series = '/series/' + s1id + '/edit'

        response = auth.post_and_redirect(change_logged_in_users_series, data=STANDARD_SERIES_ACCOUNT)

        assert 200 == response.status_code
        assert 1 == len(get_series_by_username(USERNAME1))
        date = datetime.combine(START_DATE1_DATE, datetime.min.time())
        assert 1 == len(get_transactions(USERNAME1, {'date': date}))
        assert START_DATE1_DATE == get_transactions(USERNAME1, {'date': date}).first().date
        assert ACCOUNT_NAME1 == get_transactions(USERNAME1, {'payee': ACCOUNT_NAME1}).first().payee

        a1 = {'account_name': 'ACCOUNT_NAME1'}
        a1id = get_accounts(USERNAME1, a1).first().get_id()

        change_logged_in_users_series = '/accounts/' + a1id + '/edit'

        a1 = {'account_name': ACCOUNT_NAME2}
        a1s = create_accounts(**a1)

        response = auth.post_and_redirect(change_logged_in_users_series, data=a1s[0])

        assert 200 == response.status_code

        assert 1 == len(get_accounts(USERNAME1, a1))
        assert ACCOUNT_NAME2 == get_accounts(USERNAME1, a1).first().account_name

        assert 200 == response.status_code
        assert 1 == len(get_series_by_username(USERNAME1))
        date = datetime.combine(START_DATE1_DATE, datetime.min.time())
        assert 1 == len(get_transactions(USERNAME1, {'date': date}))
        assert START_DATE1_DATE == get_transactions(USERNAME1, {'date': date}).first().date
        assert ACCOUNT_NAME2 == get_transactions(USERNAME1, {'payer': PAYER1}).first().payee
