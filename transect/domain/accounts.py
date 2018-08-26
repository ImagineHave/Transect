from mongoengine import StringField, DateTimeField, Document, BooleanField
import datetime


class Accounts(Document):
    account_name = StringField(max_length=200, required=True)
    account_opened_date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    credit_or_debit = BooleanField(default=True)
