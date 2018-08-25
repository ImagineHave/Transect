from mongoengine import (
    StringField, DecimalField, DateTimeField, ReferenceField, Document, ListField, DictField, CASCADE
    )
from transect.domain.users import Users, get_user
from transect.domain.frequencies import Frequency
from transect.domain.transactions import insert_transaction, Transactions
import datetime
from dateutil.relativedelta import relativedelta


class Series(Document):
    payer = StringField(max_length=200, required=True)
    payee = StringField(max_length=200, required=True)
    amount = DecimalField(required=True, places=2, default=0.0)
    start_date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    end_date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    user = ReferenceField(Users)
    frequency = ReferenceField(Frequency, required=True)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    transactions = ListField(ReferenceField(Transactions, reverse_delete_rule=CASCADE))

    def get_id(self):
        return str(self.id)


def create_transactions(username, payer, payee, amount, start_date, end_date, frequency):
    transactions = []
    while start_date <= end_date:
        transaction = insert_transaction(username=username, payer=payer, payee=payee, amount=amount, date=start_date)
        start_date += relativedelta(**frequency)
        transactions.append(transaction)
    return transactions


def insert_series(username, payer, payee, amount, start_date, end_date, frequency):
    user = get_user(username=username)
    transactions = create_transactions(username, payer, payee, amount, start_date, end_date, frequency.value)
    series = Series(
        user=user,
        payer=payer,
        payee=payee,
        amount=amount,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        transactions=transactions
    )
    series.save()
    return series


def get_series_by_id(_id):
    return Series.objects(id=_id).first()


def delete_series(_id):
    series = get_series_by_id(_id)
    for transaction in series.transactions:
        transaction.delete()
    series.delete()
