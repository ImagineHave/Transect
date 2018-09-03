from transect.domain.accounts import (
    insert_account, get_account_by_id, get_accounts_by_username, get_accounts, delete_account, update_account
)
from tests.conftest import (
    USERNAME1, ACCOUNT_NAME1, ACCOUNT_OPENED_DATE1, ACCOUNT_NAME2
)


def test_insert_account(app):
    with app.app_context():
        data = {
            'username': USERNAME1,
            'account_name': ACCOUNT_NAME1,
            'account_opened_date': ACCOUNT_OPENED_DATE1,
        }
        account = insert_account(data)
        assert account is not None
        assert get_account_by_id(account.id) is not None
        assert 3 == len(get_accounts_by_username(USERNAME1))
        assert 3 == len(get_accounts({'username': USERNAME1}))
        assert 1 == len(get_accounts({'username': USERNAME1, 'account_name': ACCOUNT_NAME1}))


def test_delete_account(app):
    with app.app_context():
        data = {
            'username': USERNAME1,
            'account_name': ACCOUNT_NAME1,
            'account_opened_date': ACCOUNT_OPENED_DATE1,
        }
        account = insert_account(data)
        assert account is not None
        assert get_account_by_id(account.id) is not None
        assert 3 == len(get_accounts_by_username(USERNAME1))
        assert 3 == len(get_accounts({'username': USERNAME1}))
        assert 1 == len(get_accounts({'username': USERNAME1, 'account_name': ACCOUNT_NAME1}))
        delete_account(account.id)
        assert get_account_by_id(account.id) is None
        assert 2 == len(get_accounts_by_username(USERNAME1))
        assert 2 == len(get_accounts({'username': USERNAME1, }))
        assert 0 == len(get_accounts({'username': USERNAME1, 'account_name': ACCOUNT_NAME1}))


def test_update_account(app):
    with app.app_context():
        data = {
            'username': USERNAME1,
            'account_name': ACCOUNT_NAME1,
            'account_opened_date': ACCOUNT_OPENED_DATE1,
        }
        account = insert_account(data)
        assert account is not None
        assert get_account_by_id(account.id) is not None
        assert 3 == len(get_accounts_by_username(USERNAME1))
        assert 3 == len(get_accounts({'username': USERNAME1, }))
        assert 1 == len(get_accounts({'username': USERNAME1, 'account_name': ACCOUNT_NAME1}))
        data = {
            'username': USERNAME1,
            'account_name': ACCOUNT_NAME2,
            'account_opened_date': ACCOUNT_OPENED_DATE1,
        }
        update_account(account.id, data)
        assert get_account_by_id(account.id) is not None
        assert 3 == len(get_accounts_by_username(USERNAME1))
        assert 3 == len(get_accounts({'username': USERNAME1}))
        assert 1 == len(get_accounts({'username': USERNAME1, 'account_name': ACCOUNT_NAME2}))
        assert 0 == len(get_accounts({'username': USERNAME1, 'account_name': ACCOUNT_NAME1}))
