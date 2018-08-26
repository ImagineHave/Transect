from mongoengine import StringField, DateTimeField, Document, BooleanField
import datetime


class Accounts(Document):
    account_name = StringField(max_length=200, required=True)
    account_opened_date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    credit_or_debit = BooleanField(default=True)


def create_standard_test_accounts():
    Accounts(account_name='other').save()



def get_accounts_as_list_of_tuples():
    return [(a.account_name, a.account_name) for a in Accounts.objects.order_by('account_name')]
