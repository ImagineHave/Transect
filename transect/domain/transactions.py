from bson import ObjectId
from transect.db import get_db
from transect.domain.domain import Domain
from transect.domain.users import get_user_id_from_username


class Transactions(Domain):

    def __init__(self, payer=None, payee=None, date=None, amount=None, series_id=None, _id=None):
        self.table_name = 'transactions'
        self.properties = {'payer': payer,
                           'payee': payee,
                           'date': date,
                           'amount': amount,
                           'series_id': series_id,
                           '_id': _id}


def get_transactions_for_username(username=None):
    if username:
        user_id = get_user_id_from_username(username)
        return get_db()['transactions'].find({"user_id": user_id})
    else:
        return None


def get_transactions_for_user_id(user_id=None):
    if user_id:
        return get_db()['transactions'].find({"user_id": user_id})
    else:
        return None


def get_transaction_from_transaction_id(_id):
    return get_db()['transactions'].find_one({"_id": ObjectId(_id)})


def insert_transaction(transaction):
    return get_db()['transactions'].insert_one(transaction)


def update_transaction(_id, transaction):
    return get_db()['transactions'].update({"_id": ObjectId(_id)}, transaction)


def delete_transaction(_id):
    get_db()['transactions'].remove({"_id": ObjectId(_id)})


def get_transaction_id(transaction):
    return str(get_db()['transactions'].find_one(transaction)['_id'])


def get_transaction(transaction):
    return get_db()['transactions'].find_one(transaction)
