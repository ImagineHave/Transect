from mongoengine import StringField, DateTimeField, Document, BooleanField, ReferenceField
import datetime
from transect.domain.users import get_user, Users


class Accounts(Document):
    account_name = StringField(max_length=200, required=True, unique=True)
    account_opened_date = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    user = ReferenceField(Users)

    def get_id(self):
        return str(self.id)


def create_standard_test_accounts():
    Accounts(account_name='other').save()


def get_accounts_as_list_of_tuples():
    return [(a.account_name, a.account_name) for a in Accounts.objects.order_by('account_name')]


def insert_account(data):
    data['user'] = Users.objects(username=data.pop('username')).first().id
    account = Accounts(**data)
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
    data['user'] = Users.objects(username=data.pop('username')).first().id
    account.update(**data, date_modified=datetime.datetime.utcnow)
    return account


def get_accounts(data):
    data['user'] = Users.objects(username=data.pop('username')).first().id
    accounts = Accounts.objects(__raw__=data)
    return accounts
