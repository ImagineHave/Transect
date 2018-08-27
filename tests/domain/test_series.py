from datetime import datetime
from transect.domain.series import (
    create_transactions, insert_series, get_series_by_id, delete_series, get_series_by_username, get_series, bulk_update
)
from transect.domain.transactions import get_transactions_for_username, get_transaction
from transect.domain.frequencies import Frequency
from tests.conftest import (
    USERNAME1, PAYER1, PAYEE1, AMOUNT, START_DATE1_DATE, END_DATE1_DATE, SERIES_NAME, PAYER2
)


def test_create_transactions_weekly(app):
    with app.app_context():
        frequency = Frequency.objects(label='weekly').first()
        create_transactions(USERNAME1, PAYER1, PAYEE1, AMOUNT, START_DATE1_DATE, END_DATE1_DATE, frequency)
        assert 105 == get_transactions_for_username(USERNAME1).count()


def test_create_transactions_monthly(app):
    with app.app_context():
        frequency = Frequency.objects(label='monthly').first()
        create_transactions(USERNAME1, PAYER1, PAYEE1, AMOUNT, START_DATE1_DATE, END_DATE1_DATE, frequency)
        assert 25 == get_transactions_for_username(USERNAME1).count()


def test_create_transactions_monthly_before(app):
    with app.app_context():
        end_date = datetime.strptime('1984-05-13', '%Y-%m-%d')
        frequency = Frequency.objects(label='monthly').first()
        create_transactions(USERNAME1, PAYER1, PAYEE1, AMOUNT, START_DATE1_DATE, end_date, frequency)
        assert 24 == get_transactions_for_username(USERNAME1).count()


def test_create_transactions_monthly_after(app):
    with app.app_context():
        end_date = datetime.strptime('1984-05-15', '%Y-%m-%d')
        frequency = Frequency.objects(label='monthly').first()
        create_transactions(USERNAME1, PAYER1, PAYEE1, AMOUNT, START_DATE1_DATE, end_date, frequency)
        assert 25 == get_transactions_for_username(USERNAME1).count()


def test_create_transactions_annually(app):
    with app.app_context():
        frequency = Frequency.objects(label='annually').first()
        create_transactions(USERNAME1, PAYER1, PAYEE1, AMOUNT, START_DATE1_DATE, END_DATE1_DATE, frequency)
        assert 3 == get_transactions_for_username(USERNAME1).count()


def test_insert_series(app):
    with app.app_context():
        frequency = Frequency.objects(label='monthly').first()
        series = insert_series(
            USERNAME1,
            SERIES_NAME,
            PAYER1,
            PAYEE1,
            AMOUNT,
            START_DATE1_DATE,
            END_DATE1_DATE,
            frequency)
        assert 25 == get_transactions_for_username(USERNAME1).count()
        assert series is not None
        assert 25 == len(series.transactions)
        assert get_series_by_id(series.id) is not None
        assert 25 == len(get_series_by_id(series.id).transactions)
        assert 1 == len(get_series_by_username(USERNAME1))
        assert 1 == len(get_series(USERNAME1, {}))
        assert 1 == len(get_series(USERNAME1, {'payer': PAYER1}))


def test_delete_series(app):
    with app.app_context():
        frequency = Frequency.objects(label='monthly').first()
        series = insert_series(
            USERNAME1,
            SERIES_NAME,
            PAYER1,
            PAYEE1,
            AMOUNT,
            START_DATE1_DATE,
            END_DATE1_DATE,
            frequency)
        assert 25 == get_transactions_for_username(USERNAME1).count()
        assert series is not None
        transactions = series.transactions
        assert 25 == len(transactions)
        assert get_series_by_id(series.id) is not None
        assert 25 == len(get_series_by_id(series.id).transactions)
        assert 1 == len(get_series_by_username(USERNAME1))
        assert 1 == len(get_series(USERNAME1, {}))
        assert 1 == len(get_series(USERNAME1, {'payer': PAYER1}))
        delete_series(series.id)
        assert get_series_by_id(series.id) is None
        assert 0 == len(get_series_by_username(USERNAME1))
        assert get_transaction(transactions[0].id) is None
        assert 0 == len(get_series(USERNAME1, {}))
        assert 0 == len(get_series(USERNAME1, {'payer': PAYER1}))


def test_bulk_update(app):
    with app.app_context():
        frequency = Frequency.objects(label='monthly').first()
        series = insert_series(
            USERNAME1,
            SERIES_NAME,
            PAYER1,
            PAYEE1,
            AMOUNT,
            START_DATE1_DATE,
            END_DATE1_DATE,
            frequency)
        assert 25 == get_transactions_for_username(USERNAME1).count()
        assert series is not None
        assert 25 == len(series.transactions)
        assert get_series_by_id(series.id) is not None
        assert 25 == len(get_series_by_id(series.id).transactions)
        assert 1 == len(get_series_by_username(USERNAME1))
        assert 1 == len(get_series(USERNAME1, {}))
        assert 1 == len(get_series(USERNAME1, {'payer': PAYER1}))

        from_data = {'payer': PAYER1}
        to_data = {'payer': PAYER2}

        bulk_update(USERNAME1, from_data, to_data)
        assert 25 == get_transactions_for_username(USERNAME1).count()
        assert series is not None
        assert 25 == len(series.transactions)
        assert get_series_by_id(series.id) is not None
        assert 25 == len(get_series_by_id(series.id).transactions)
        assert 1 == len(get_series_by_username(USERNAME1))
        assert 1 == len(get_series(USERNAME1, {}))
        assert 1 == len(get_series(USERNAME1, {'payer': PAYER2}))
        for transaction in get_series_by_id(series.id).transactions:
            assert PAYER2 == transaction.payer
