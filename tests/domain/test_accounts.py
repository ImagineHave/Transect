from transect.domain.accounts import (
    insert_account, get_account_by_id, get_accounts_by_username, get_accounts, delete_account, update_account
)
from datetime import datetime


def test_insert_account(app):
    with app.app_context():
        account_name = 'ACCOUNT'
        account_opened_date = datetime.utcnow
        credit_or_debit = True
        username = 'test'
        data = {
            'account_name': account_name,
            'account_opened_date': account_opened_date,
            'credit_or_debit': credit_or_debit
        }
        account = insert_account(username, data)
        assert account is not None
        assert get_account_by_id(account.id) is not None
        assert 1 == len(get_accounts_by_username(username))
        assert 1 == len(get_accounts(username, {}))
        assert 1 == len(get_accounts(username, {'account_name': account_name}))


def test_delete_account(app):
    with app.app_context():
        account_name = 'ACCOUNT'
        account_opened_date = datetime.utcnow
        credit_or_debit = True
        username = 'test'
        data = {
            'account_name': account_name,
            'account_opened_date': account_opened_date,
            'credit_or_debit': credit_or_debit
        }
        account = insert_account(username, data)
        assert account is not None
        assert get_account_by_id(account.id) is not None
        assert 1 == len(get_accounts_by_username(username))
        assert 1 == len(get_accounts(username, {}))
        assert 1 == len(get_accounts(username, {'account_name': account_name}))
        delete_account(account.id)
        assert get_account_by_id(account.id) is None
        assert 0 == len(get_accounts_by_username(username))
        assert 0 == len(get_accounts(username, {}))
        assert 0 == len(get_accounts(username, {'account_name': account_name}))


def test_update_account(app):
    with app.app_context():
        account_name = 'ACCOUNT1'
        account_opened_date = datetime.utcnow
        credit_or_debit = True
        username = 'test'
        data = {
            'account_name': account_name,
            'account_opened_date': account_opened_date,
            'credit_or_debit': credit_or_debit
        }
        account = insert_account(username, data)
        assert account is not None
        assert get_account_by_id(account.id) is not None
        assert 1 == len(get_accounts_by_username(username))
        assert 1 == len(get_accounts(username, {}))
        assert 1 == len(get_accounts(username, {'account_name': account_name}))
        account_name = 'ACCOUNT1'
        account_opened_date = datetime.utcnow
        credit_or_debit = False
        data = {
            'account_name': account_name,
            'account_opened_date': account_opened_date,
            'credit_or_debit': credit_or_debit
        }
        update_account(account.id, data)
        assert get_account_by_id(account.id) is not None
        assert 1 == len(get_accounts_by_username(username))
        assert 1 == len(get_accounts(username, {}))
        assert 1 == len(get_accounts(username, {'account_name': account_name}))