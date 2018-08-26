from datetime import datetime
from transect.domain.series import (
    create_transactions, insert_series, get_series_by_id, delete_series, get_series_by_username, get_series
)
from transect.domain.transactions import get_transactions_for_username, get_transaction
from transect.domain.frequencies import get_by_label


def test_create_transactions_weekly(app):
    with app.app_context():
        username = 'test'
        payer = 'Payer'
        payee = 'Payee'
        amount = 123.45
        start_date = datetime.strptime('1982-05-14', '%Y-%m-%d')
        end_date = datetime.strptime('1984-05-14', '%Y-%m-%d')
        frequency = get_by_label('weekly')
        create_transactions(username, payer, payee, amount, start_date, end_date, frequency)
        assert 105 == get_transactions_for_username(username).count()


def test_create_transactions_monthly(app):
    with app.app_context():
        username = 'test'
        payer = 'Payer'
        payee = 'Payee'
        amount = 123.45
        start_date = datetime.strptime('1982-05-14', '%Y-%m-%d')
        end_date = datetime.strptime('1984-05-14', '%Y-%m-%d')
        frequency = get_by_label('monthly')
        create_transactions(username, payer, payee, amount, start_date, end_date, frequency)
        assert 25 == get_transactions_for_username(username).count()


def test_create_transactions_monthly_before(app):
    with app.app_context():
        username = 'test'
        payer = 'Payer'
        payee = 'Payee'
        amount = 123.45
        start_date = datetime.strptime('1982-05-14', '%Y-%m-%d')
        end_date = datetime.strptime('1984-05-13', '%Y-%m-%d')
        frequency = get_by_label('monthly')
        create_transactions(username, payer, payee, amount, start_date, end_date, frequency)
        assert 24 == get_transactions_for_username(username).count()


def test_create_transactions_annually(app):
    with app.app_context():
        username = 'test'
        payer = 'Payer'
        payee = 'Payee'
        amount = 123.45
        start_date = datetime.strptime('1982-05-14', '%Y-%m-%d')
        end_date = datetime.strptime('1984-05-14', '%Y-%m-%d')
        frequency = get_by_label('annually')
        create_transactions(username, payer, payee, amount, start_date, end_date, frequency)
        assert 3 == get_transactions_for_username(username).count()


def test_create_transactions_monthly_before(app):
    with app.app_context():
        username = 'test'
        payer = 'Payer'
        payee = 'Payee'
        amount = 123.45
        start_date = datetime.strptime('1982-05-14', '%Y-%m-%d')
        end_date = datetime.strptime('1984-05-15', '%Y-%m-%d')
        frequency = get_by_label('monthly')
        create_transactions(username, payer, payee, amount, start_date, end_date, frequency)
        assert 25 == get_transactions_for_username(username).count()


def test_insert_series(app):
    with app.app_context():
        name = 'series'
        username = 'test'
        payer = 'Payer'
        payee = 'Payee'
        amount = 123.45
        start_date = datetime.strptime('1982-05-14', '%Y-%m-%d')
        end_date = datetime.strptime('1984-05-14', '%Y-%m-%d')
        frequency = get_by_label('monthly')
        series = insert_series(username, name, payer, payee, amount, start_date, end_date, frequency)
        assert 25 == get_transactions_for_username(username).count()
        assert series is not None
        assert 25 == len(series.transactions)
        assert get_series_by_id(series.id) is not None
        assert 25 == len(get_series_by_id(series.id).transactions)
        assert 1 == len(get_series_by_username(username))
        assert 1 == len(get_series(username, {}))
        assert 1 == len(get_series(username, {'payer': payer}))


def test_delete_series(app):
    with app.app_context():
        name = 'series'
        username = 'test'
        payer = 'Payer'
        payee = 'Payee'
        amount = 123.45
        start_date = datetime.strptime('1982-05-14', '%Y-%m-%d')
        end_date = datetime.strptime('1984-05-14', '%Y-%m-%d')
        frequency = get_by_label('monthly')
        series = insert_series(username, name, payer, payee, amount, start_date, end_date, frequency)
        assert 25 == get_transactions_for_username(username).count()
        assert series is not None
        transactions = series.transactions
        assert 25 == len(transactions)
        assert get_series_by_id(series.id) is not None
        assert 25 == len(get_series_by_id(series.id).transactions)
        assert 1 == len(get_series_by_username(username))
        assert 1 == len(get_series(username, {}))
        assert 1 == len(get_series(username, {'payer': payer}))
        delete_series(series.id)
        assert get_series_by_id(series.id) is None
        assert 0 == len(get_series_by_username(username))
        assert get_transaction(transactions[0].id) is None
        assert 0 == len(get_series(username, {}))
        assert 0 == len(get_series(username, {'payer': payer}))
