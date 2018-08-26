from datetime import datetime
from transect.domain.frequencies import get_by_label
from transect.domain.transactions import get_transactions_for_user_id, get_transactions


def create_series(
        username='test',
        payer='Payer',
        payee='Payee',
        amount=123.45,
        start_date=datetime.strptime('1982-05-14', '%Y-%m-%d'),
        end_date=datetime.strptime('1984-05-14', '%Y-%m-%d'),
        frequency='monthly',
        count=1):

    series = []
    for i in range(count):
        s = {
            'username': username,
            'payer': payer,
            'payee': payee,
            'amount': amount,
            'start_date': start_date.date(),
            'end_date': end_date.date(),
            'frequency': get_by_label(frequency)
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
            response = auth.post('/series/add', data=series)
            print(response.data)

        assert len(get_transactions_for_user_id(user_id1)) == 5

        for series in s1s:
            dt = datetime.combine(series['date'], datetime.min.time())
            assert len(get_transactions(series['username'], {'date': dt})) == 1
            assert get_transactions(series['username'], {'date': dt}).first().date.date() == series['date']