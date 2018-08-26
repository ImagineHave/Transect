import datetime
from decimal import ROUND_HALF_UP
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import InputRequired


class AddForm(FlaskForm):
    payer = StringField('payer', [InputRequired()])
    payee = StringField('payee', [InputRequired()])
    amount = DecimalField('amount', [InputRequired()], places=2, default=0.0, rounding=ROUND_HALF_UP)
    date = DateField('date', [InputRequired()], format='%Y-%m-%d', default=datetime.date.today())
    submit = SubmitField('add')
