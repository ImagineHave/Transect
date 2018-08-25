from bson import ObjectId
from transect.db import get_db
from flask.ext.mongoengine.wtf import model_form
from transect.domain.users import get_user
from mongoengine import StringField, DecimalField, DateTimeField, ReferenceField, Document
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
    return Transactions.objects(user=user)


def get_transactions_for_username(username=None):
    if username:
        user = get_user(username=username)
        return Transactions.objects(user=user.id)
    else:
        return None


def get_transactions_for_user_id(user_id=None):
    if user_id:
        user = get_user(_id=user_id)
        return Transactions.objects(user=user)
    else:
        return None


def get_transaction_from_transaction_id(_id):
    return Transactions.objects(id=_id).first()


def insert_transaction(username, payer, payee, amount, date):
    user = get_user(username=username)
    transaction = Transactions(user=user, payer=payer, payee=payee, amount=amount, date=date)
    transaction.save()


def update_transaction(_id, username=None, payer=None, payee=None, amount=None, date=None):
    transaction = get_transaction_from_transaction_id(_id)
    if username is not None:
        user = get_user(username=username)
        transaction.update(user=user)
    if payer is not None:
        transaction.update(payer=payer)
    if payee is not None:
        transaction.update(payee=payee)
    if amount is not None:
        transaction.update(amount=amount)
    if date is not None:
        transaction.update(date=date)
    transaction.update(date_modified=datetime.datetime.utcnow)


def delete_transaction(_id):
    transaction = get_transaction_from_transaction_id(_id)
    transaction.delete()


def get_transaction(_id):
    transaction = Transactions.objects(id=_id).first()
    return transaction


def get_transactions(username, data):
    user = get_user(username=username)
    transactions = Transactions.objects(user=user, __raw__=data)
    return transactions


TransactionsForm = model_form(Transactions)
