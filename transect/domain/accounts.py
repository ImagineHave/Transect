from mongoengine import StringField, DateTimeField, Document, BooleanField, ReferenceField
import datetime
from transect.domain.users import get_user, Users


class Accounts(Document):
    account_name = StringField(max_length=200, required=True)
    account_opened_date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    credit_or_debit = BooleanField(default=True)
    user = ReferenceField(Users)

    def get_id(self):
        return str(self.id)


def create_standard_test_accounts():
    Accounts(account_name='other').save()


def get_accounts_as_list_of_tuples():
    return [(a.account_name, a.account_name) for a in Accounts.objects.order_by('account_name')]


def insert_account(username, data):
    user = get_user(username=username)
    account = Accounts(user=user, **data)
    account.save()
    return account


def get_accounts_by_username(username):
    return Accounts.objects(user__in=Users.objects.filter(username=username)).order_by('account_name')


def get_account_by_id(_id):
    return Accounts.objects(id=_id).first()


def delete_account(_id):
    account = get_account_by_id(_id)
    account.delete()


def update_account(_id, data):
    account = get_account_by_id(_id)
    account.update(**data, date_modified=datetime.datetime.utcnow)
    return account


def get_accounts(username, data):
    user = get_user(username=username)
    account = Accounts.objects(user=user, __raw__=data)
    return account
