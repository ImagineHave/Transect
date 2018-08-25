from mongoengine import StringField, DecimalField, DateTimeField, ReferenceField, Document
from transect.domain.users import Users, get_user
from transect.domain.transactions import insert_transaction
import datetime
from dateutil.relativedelta import relativedelta

FREQ_CHOICES = [('Weekly', {'weeks': 1}), ('Monthly', {'months': 1}), ('Annually', {'years': 1})]


class Series(Document):
    payer = StringField(max_length=200, required=True)
    payee = StringField(max_length=200, required=True)
    amount = DecimalField(required=True, places=2, default=0.0)
    start_date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    end_date = DateTimeField(required=True, default=datetime.datetime.utcnow)
    user = ReferenceField(Users)
    frequency = StringField(required=True, default='Monthly')
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

    def get_id(self):
        return str(self.id)


def create_transactions(username, payer, payee, amount, start_date, end_date, frequency):
    transactions = []
    for i in range(count):
        dt = datetime.strptime(date, '%Y-%m-%d') + relativedelta(months=i)
        t = {'username': username, 'payer': payer, 'payee': payee, 'amount': amount+(i*10), 'date': dt.date()}
        insert_transaction(t)
    return transactions


def insert_series(username, payer, payee, amount, start_date, frequency):
    user = get_user(username=username)
    series = Series(
        user=user,
        payer=payer,
        payee=payee,
        amount=amount,
        start_date=start_date,
        frequency=frequency
    )
    series.save()
