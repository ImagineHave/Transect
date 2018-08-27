from bson import ObjectId
from dateutil.relativedelta import relativedelta
from transect.domain.transactions import insert_transaction, get_transactions, update_transaction, delete_transaction, \
    get_transactions_for_username, get_transactions_for_user_id, get_transaction, Transactions, bulk_update
from tests.conftest import (
    USERNAME1, USERNAME2, PAYER1, PAYEE1, AMOUNT, START_DATE1_DATE, PAYER2, PAYEE2
)


def create_transactions(payer=PAYER1, payee=PAYEE1, amount=AMOUNT, date=START_DATE1_DATE, count=1):
    transactions = []
    for i in range(count):
        date += relativedelta(months=i)
        t = {'payer': payer, 'payee': payee, 'amount': amount+(10*i), 'date': date.date()}
        transactions.append(t)
    return transactions


def test_insert_transaction(app, test_user):
    with app.app_context():

        t1s = create_transactions(count=5)
        t2s = create_transactions(count=3)

        for transaction in t1s:
            insert_transaction(USERNAME1, transaction)

        for transaction in t2s:
            insert_transaction(USERNAME2, transaction)

        user_id1 = test_user.get_user_id(USERNAME1)
        user_id2 = test_user.get_user_id(USERNAME2)

        ts1 = Transactions.objects(**{'user': ObjectId(user_id1)})
        ts2 = Transactions.objects(**{'user': ObjectId(user_id2)})

        assert 5 == ts1.count()
        assert 3 == ts2.count()


def test_get_transactions(app, test_user):
    t1 = create_transactions()[0]
    with app.app_context():
        insert_transaction(USERNAME1, t1)
        t2 = get_transactions(USERNAME1, {'date': START_DATE1_DATE}).first()
        assert t2 is not None
        assert t1['date'] == t2['date'].date()


def test_update_transaction(app, test_user):
    with app.app_context():
        user_id1 = test_user.get_user_id(USERNAME1)
        user_id2 = test_user.get_user_id(USERNAME2)

        t1s = create_transactions(count=5)
        t2s = create_transactions(count=3)

        for transaction in t1s:
            insert_transaction(USERNAME1, transaction)

        for transaction in t2s:
            insert_transaction(USERNAME2, transaction)

        ts1 = Transactions.objects(**{'user': ObjectId(user_id1)})
        ts2 = Transactions.objects(**{'user': ObjectId(user_id2)})

        assert ts1.count() == 5
        assert ts2.count() == 3

        t = Transactions.objects(**{'user': ObjectId(user_id1), 'payer': PAYER1}).first()
        tid = t.get_id()

        t4 = create_transactions(payer=PAYER2, payee=PAYEE2)[0]

        update_transaction(tid, t4)

        ts1 = Transactions.objects(**{'user': ObjectId(user_id1)})
        ts2 = Transactions.objects(**{'user': ObjectId(user_id2)})

        assert ts1.count() == 5
        assert ts2.count() == 3

        t = Transactions.objects(**{'user': ObjectId(user_id1), 'payee': PAYEE2}).first()
        assert t.payee == PAYEE2
        assert Transactions.objects(**{'user': ObjectId(user_id2), 'payee': PAYEE2}).count() == 0


def test_delete_transaction(app, test_user):
    with app.app_context():
        user_id1 = ObjectId(test_user.get_user_id(USERNAME1))
        user_id2 = ObjectId(test_user.get_user_id(USERNAME2))

        t1s = create_transactions(count=5)
        t2s = create_transactions(count=3)

        for transaction in t1s:
            insert_transaction(USERNAME1, transaction)

        for transaction in t2s:
            insert_transaction(USERNAME2, transaction)

        ts1 = Transactions.objects(**{'user': ObjectId(user_id1)})
        ts2 = Transactions.objects(**{'user': ObjectId(user_id2)})

        assert ts1.count() == 5
        assert ts2.count() == 3

        t = Transactions.objects(**{'user': ObjectId(user_id1), 'payer': PAYER1}).first()
        tid = t.get_id()

        delete_transaction(tid)

        ts1 = Transactions.objects(**{'user': ObjectId(user_id1)})
        ts2 = Transactions.objects(**{'user': ObjectId(user_id2)})

        assert ts1.count() == 4
        assert ts2.count() == 3


def test_get_transaction_id(app, test_user):
    with app.app_context():
        user_id1 = ObjectId(test_user.get_user_id(USERNAME1))
        ts = create_transactions()
        for transaction in ts:
            insert_transaction(USERNAME1, transaction)

        tid = Transactions.objects(**{'user': ObjectId(user_id1)}).first().id
        assert Transactions.objects(**{'user': ObjectId(user_id1)}).first().id == get_transaction(tid).id


def test_get_transactions_for_username(app, test_user):
    with app.app_context():

        t1s = create_transactions(count=3)
        t2s = create_transactions(count=4)

        for transaction in t1s:
            insert_transaction(USERNAME1, transaction)

        for transaction in t2s:
            insert_transaction(USERNAME2, transaction)

        ts1 = get_transactions_for_username(USERNAME1)
        ts2 = get_transactions_for_username(USERNAME2)

        assert ts1.count() == 3
        assert ts2.count() == 4


def test_get_transactions_for_user_id(app, test_user):
    with app.app_context():
        user_id1 = ObjectId(test_user.get_user_id(USERNAME1))
        user_id2 = ObjectId(test_user.get_user_id(USERNAME2))

        t1s = create_transactions(count=3)
        t2s = create_transactions(count=4)

        for transaction in t1s:
            insert_transaction(USERNAME1, transaction)

        for transaction in t2s:
            insert_transaction(USERNAME2, transaction)

        ts1 = get_transactions_for_user_id(user_id1)
        ts2 = get_transactions_for_user_id(user_id2)

        assert ts1.count() == 3
        assert ts2.count() == 4


def test_bulk_update(app, test_user):
    with app.app_context():

        t1s = create_transactions(count=5)
        t2s = create_transactions(count=3)

        for transaction in t1s:
            insert_transaction(USERNAME1, transaction)

        for transaction in t2s:
            insert_transaction(USERNAME2, transaction)

        user_id1 = test_user.get_user_id(USERNAME1)
        user_id2 = test_user.get_user_id(USERNAME2)

        ts1 = Transactions.objects(**{'user': ObjectId(user_id1)})
        ts2 = Transactions.objects(**{'user': ObjectId(user_id2)})

        assert 5 == ts1.count()
        assert 3 == ts2.count()

        from_data = {'payer': PAYER1}
        to_data = {'payer': PAYER2}
        bulk_update(USERNAME1, from_data, to_data)

        ts1 = Transactions.objects(**{'user': ObjectId(user_id1)})
        ts2 = Transactions.objects(**{'user': ObjectId(user_id2)})

        assert 5 == ts1.count()
        assert 3 == ts2.count()

        for t in ts1:
            assert PAYER2 == t.payer

        for t in ts2:
            assert PAYER1 == t.payer



