from transect.domain.users import get_user
from mongoengine import (
    DecimalField, DateTimeField, ReferenceField, Document
)
from transect.domain.users import Users
from transect.domain.accounts import Accounts
import datetime
import copy


class Transactions(Document):
    payer = ReferenceField(Accounts, required=True)
    payee = ReferenceField(Accounts, required=True)
    amount = DecimalField(required=True, places=2, default=0.0)
    date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    user = ReferenceField(Users, required=True)
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


def insert_transaction(data):
    data['user'] = Users.objects(username=data.pop('username')).first()
    data['payee'] = Accounts.objects(account_name=data.pop('payee')).first()
    data['payer'] = Accounts.objects(account_name=data.pop('payer')).first()
    transaction = Transactions(**data)
    transaction.save()
    return transaction


def update_transaction(_id, data):
    transaction = get_transaction_from_transaction_id(_id)

    data['user'] = Users.objects(username=data.pop('username')).first()
    if data['user'] != transaction.user:
        return None

    payer = Accounts.objects(account_name=data.pop('payer', None)).first()
    if payer is not None:
        data['payer'] = payer

    payee = Accounts.objects(account_name=data.pop('payee', None)).first()
    if payee is not None:
        data['payee'] = payee

    transaction.update(**data, date_modified=datetime.datetime.utcnow)
    return transaction


def delete_transaction(_id):
    transaction = get_transaction_from_transaction_id(_id)
    transaction.delete()


def get_transaction(_id):
    return Transactions.objects(id=_id).first()


def get_transactions(data):
    data['user'] = Users.objects(username=data.pop('username')).first().id

    payer = Accounts.objects(account_name=data.pop('payer', None)).first()
    if payer is not None:
        data['payer'] = payer.id

    payee = Accounts.objects(account_name=data.pop('payee', None)).first()
    if payee is not None:
        data['payee'] = payee.id

    return Transactions.objects(__raw__=data)


def get_transaction_ids(data):
    ids = []

    user = Users.objects(username=data.pop('username')).first()
    data['user'] = user.id

    payer = Accounts.objects(user=user, account_name=data.pop('payer', None)).first()
    if payer is not None:
        data['payer'] = payer.id

    payee = Accounts.objects(user=user, account_name=data.pop('payee', None)).first()
    if payee is not None:
        data['payee'] = payee.id

    for transaction in Transactions.objects(__raw__=data):
        ids.append(transaction.id)
    return ids


def bulk_update(from_data, to_data):
    for _id in get_transaction_ids(from_data):
        data = copy.deepcopy(to_data)
        update_transaction(_id, data)
