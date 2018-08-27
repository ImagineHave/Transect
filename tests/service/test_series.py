from datetime import datetime
from transect.domain.frequencies import get_by_label
from transect.domain.transactions import get_transactions_for_user_id, get_transactions
from transect.domain.series import get_series_by_username, get_series


def create_series(
        name='series name',
        username='test',
        payer='Payer',
        payee='Payee',
        amount=123.45,
        start_date='1982-05-14',
        end_date='1984-05-14',
        frequency='monthly',
        count=1):

    series = []
    for i in range(count):
        s = {
            'name': name,
            'username': username,
            'payer': payer,
            'payee': payee,
            'amount': amount,
            'start_date': datetime.strptime(start_date, '%Y-%m-%d').date(),
            'end_date': datetime.strptime(end_date, '%Y-%m-%d').date(),
            'frequency': get_by_label(frequency).label
        }
        series.append(s)
    return series


def test_adding_series(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        username1 = 'test'
        user_id1 = test_user.get_user_id(username1)

        s1s = create_series()
        assert 1 == len(s1s)

        for series in s1s:
            auth.post('/series/add', data=series)

        assert 1 == len(get_series_by_username(username1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        for series in s1s:
            dt = datetime.combine(series['start_date'], datetime.min.time())
            assert 1 == len(get_transactions(series['username'], {'date': dt}))
            assert series['start_date'] == get_transactions(series['username'], {'date': dt}).first().date.date()


def test_adding_series_accounts(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        username1 = 'test'
        user_id1 = test_user.get_user_id(username1)

        s1s = create_series(payee='')
        assert 1 == len(s1s)

        for series in s1s:
            auth.post('/series/add', data=series)

        assert 1 == len(get_series_by_username(username1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        for series in s1s:
            dt = datetime.combine(series['start_date'], datetime.min.time())
            assert 1 == len(get_transactions(series['username'], {'date': dt, 'payee': 'other'}))
            assert series['start_date'] == get_transactions(series['username'],
                                                            {'date': dt, 'payee': 'other'}).first().date.date()


def test_editing_series(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        username1 = 'test'
        user_id1 = test_user.get_user_id(username1)

        s1s = create_series()
        assert 1 == len(s1s)

        for series in s1s:
            auth.post('/series/add', data=series)

        assert 1 == len(get_series_by_username(username1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        s1 = {'payee': 'Payee'}
        s1id = get_series(username1, s1).first().get_id()

        change_logged_in_users_series = '/series/' + s1id + '/edit'

        s1s = create_series(payee='Payee2', start_date='1952-05-14')

        response = auth.post_and_redirect(change_logged_in_users_series, data=s1s[0])

        assert 200 == response.status_code

        for series in s1s:
            dt = datetime.combine(series['start_date'], datetime.min.time())
            assert 1 == len(get_transactions(series['username'], {'date': dt}))
            assert series['start_date'] == get_transactions(series['username'], {'date': dt}).first().date.date()


def test_editing_series_accounts(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        username1 = 'test'
        user_id1 = test_user.get_user_id(username1)

        s1s = create_series()
        assert 1 == len(s1s)

        for series in s1s:
            auth.post('/series/add', data=series)

        assert 1 == len(get_series_by_username(username1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        s1 = {'payee': 'Payee'}
        s1id = get_series(username1, s1).first().get_id()

        change_logged_in_users_series = '/series/' + s1id + '/edit'

        s1s = create_series(payee='', start_date='1952-05-14')

        response = auth.post_and_redirect(change_logged_in_users_series, data=s1s[0])

        assert 200 == response.status_code

        for series in s1s:
            dt = datetime.combine(series['start_date'], datetime.min.time())
            assert 1 == len(get_transactions(series['username'], {'date': dt, 'payee': 'other'}))
            assert series['start_date'] == get_transactions(series['username'],
                                                            {'date': dt, 'payee': 'other'}).first().date.date()


def test_deleting_series(client, app, auth, test_user):
    with app.app_context():
        add = '/series/add'
        response = auth.post_and_redirect(add)
        assert b"login" in response.data
        assert b"register" in response.data

        auth.login()
        response = auth.post_and_redirect(add)
        assert b"add" in response.data

        username1 = 'test'
        user_id1 = test_user.get_user_id(username1)

        s1s = create_series()
        assert 1 == len(s1s)

        for series in s1s:
            response = auth.post_and_redirect('/series/add', data=series)
            assert b"all" in response.data

        assert 1 == len(get_series_by_username(username1))
        assert 25 == len(get_transactions_for_user_id(user_id1))

        s1 = {'payee': 'Payee'}
        s1id = get_series(username1, s1).first().get_id()

        change_logged_in_users_series = '/series/' + s1id + '/delete'

        response = auth.post_and_redirect(change_logged_in_users_series)

        assert 200 == response.status_code

        for series in s1s:
            dt = datetime.combine(series['start_date'], datetime.min.time())
            assert 0 == len(get_transactions(series['username'], {'date': dt}))
