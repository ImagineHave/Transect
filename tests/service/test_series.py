from datetime import datetime
from transect.domain.transactions import get_transactions_for_user_id, get_transactions
from transect.domain.series import get_series_by_username, get_series
from tests.conftest import (
    USERNAME1, PAYEE1, START_DATE1_DATE, START_DATE2_DATE,
    STANDARD_SERIES1, STANDARD_SERIES_NO_PAYER, STANDARD_SERIES2
)


def test_adding_series(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)

        response = auth.post_and_redirect('/series/add', data=STANDARD_SERIES1)
        assert 200 == response.status_code
        assert b"all" in response.data

        assert 1 == len(get_series_by_username(USERNAME1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        date = datetime.combine(START_DATE1_DATE, datetime.min.time())
        assert 1 == len(get_transactions({'username': USERNAME1, 'date': date}))
        assert START_DATE1_DATE == get_transactions({'username': USERNAME1, 'date': date}).first().date


def test_adding_series_accounts(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)

        response = auth.post_and_redirect('/series/add', data=STANDARD_SERIES_NO_PAYER)
        assert 200 == response.status_code
        assert b"all" in response.data

        assert 1 == len(get_series_by_username(USERNAME1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        date = datetime.combine(START_DATE1_DATE, datetime.min.time())
        assert 1 == len(get_transactions({'username': USERNAME1, 'date': date, 'payer': 'other'}))
        assert START_DATE1_DATE == get_transactions({'username': USERNAME1, 'date': date, 'payer': 'other'}).first().date


def test_editing_series(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)

        response = auth.post_and_redirect('/series/add', data=STANDARD_SERIES1)
        assert 200 == response.status_code
        assert b"all" in response.data

        assert 1 == len(get_series_by_username(USERNAME1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        s1 = {'payee': PAYEE1}
        s1id = get_series(USERNAME1, s1).first().get_id()

        change_logged_in_users_series = '/series/' + s1id + '/edit'

        response = auth.post_and_redirect(change_logged_in_users_series, data=STANDARD_SERIES2)

        assert 200 == response.status_code
        assert 1 == len(get_series_by_username(USERNAME1))
        date = datetime.combine(START_DATE2_DATE, datetime.min.time())
        assert 1 == len(get_transactions({'username': USERNAME1, 'date': date}))
        assert START_DATE2_DATE == get_transactions({'username': USERNAME1, 'date': date}).first().date


def test_editing_series_accounts(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)

        response = auth.post_and_redirect('/series/add', data=STANDARD_SERIES1)
        assert 200 == response.status_code
        assert b"all" in response.data

        assert 1 == len(get_series_by_username(USERNAME1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        s1 = {'payee': PAYEE1}
        s1id = get_series(USERNAME1, s1).first().get_id()

        change_logged_in_users_series = '/series/' + s1id + '/edit'

        response = auth.post_and_redirect(change_logged_in_users_series, data=STANDARD_SERIES_NO_PAYER)

        assert 200 == response.status_code

        date = datetime.combine(START_DATE1_DATE, datetime.min.time())
        assert 1 == len(get_transactions({'username': USERNAME1, 'date': date, 'payer': 'other'}))
        assert START_DATE1_DATE == get_transactions({'username': USERNAME1, 'date': date, 'payer': 'other'}).first().date


def test_deleting_series(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        user_id1 = test_user.get_user_id(USERNAME1)

        response = auth.post_and_redirect('/series/add', data=STANDARD_SERIES1)
        assert b"all" in response.data

        assert 1 == len(get_series_by_username(USERNAME1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        s1 = {'payee': PAYEE1}
        s1id = get_series(USERNAME1, s1).first().get_id()

        change_logged_in_users_series = '/series/' + s1id + '/delete'

        response = auth.post_and_redirect(change_logged_in_users_series)

        assert 200 == response.status_code

        dt = datetime.combine(START_DATE1_DATE, datetime.min.time())
        assert 0 == len(get_transactions({'username': USERNAME1, 'date': dt}))
