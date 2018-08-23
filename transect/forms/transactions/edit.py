from decimal import ROUND_HALF_UP
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import InputRequired


class EditForm(FlaskForm):
    payer = StringField('payer', [InputRequired()])
    payee = StringField('payee', [InputRequired()])
    amount = DecimalField('amount', [InputRequired()], places=2, default=0.0, rounding=ROUND_HALF_UP)
    date = DateField('date', [InputRequired()], format='%Y-%m-%d')
    submit = SubmitField('edit')
