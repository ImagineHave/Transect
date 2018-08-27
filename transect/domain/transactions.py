from transect.domain.users import get_user
from mongoengine import (
    StringField, DecimalField, DateTimeField, ReferenceField, Document
)
from transect.domain.users import Users
import datetime


class Transactions(Document):
    payer = StringField(max_length=200, required=True)
    payee = StringField(max_length=200, required=True)
    amount = DecimalField(required=True, places=2, default=0.0)
    date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    user = ReferenceField(Users)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

    def get_id(self):
        return str(self.id)


def get_transactions_for_user(user):
    return Transactions.objects(user=user).order_by('date')


def get_transactions_for_username(username=None):
    if username:
        user = get_user(username=username)
        return Transactions.objects(user=user.id).order_by('date')
    else:
        return None


def get_transactions_for_user_id(user_id=None):
    if user_id:
        user = get_user(_id=user_id)
        return Transactions.objects(user=user).order_by('date')
    else:
        return None


def get_transaction_from_transaction_id(_id):
    return Transactions.objects(id=_id).first()


def insert_transaction(username, data):
    user = get_user(username=username)
    transaction = Transactions(user=user, **data)
    transaction.save()
    return transaction


def update_transaction(_id, data):
    transaction = get_transaction_from_transaction_id(_id)
    transaction.update(**data, date_modified=datetime.datetime.utcnow)
    return transaction


def delete_transaction(_id):
    transaction = get_transaction_from_transaction_id(_id)
    transaction.delete()


def get_transaction(_id):
    return Transactions.objects(id=_id).first()


def get_transactions(username, data):
    user = get_user(username=username)
    transactions = Transactions.objects(user=user, __raw__=data)
    return transactions


def get_transaction_ids(username, data):
    ids = []
    user = get_user(username=username)
    for transaction in Transactions.objects(user=user, __raw__=data):
        ids.append(transaction.id)
    return ids


def bulk_update(username, from_data, to_data):
    for _id in get_transaction_ids(username, from_data):
        update_transaction(_id, to_data)
