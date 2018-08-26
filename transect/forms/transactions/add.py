from decimal import ROUND_HALF_UP
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField, DecimalField, SelectField, ValidationError
from wtforms.validators import InputRequired
from transect.domain.accounts import get_accounts_as_list_of_tuples


def has_payer(form, field):
    if len(form.payer_account.data) == 0 and len(field.payer.data) == 0:
        raise ValidationError('payer required.')


def has_payee(form, field):
    if len(form.payee_account.data) == 0 and len(field.payee.data) == 0:
        raise ValidationError('payee required.')


class AddForm(FlaskForm):
    payer = StringField('payer', [has_payer])
    payer_account = SelectField(label='pay from account', choices=get_accounts_as_list_of_tuples(), default='other')
    payee = StringField('payee', [has_payee])
    payee_account = SelectField(label='pay to account', choices=get_accounts_as_list_of_tuples(), default='other')
    amount = DecimalField('amount', [InputRequired()], places=2, default=0.0, rounding=ROUND_HALF_UP)
    date = DateField('date', [InputRequired()], format='%Y-%m-%d')
    submit = SubmitField('add')

