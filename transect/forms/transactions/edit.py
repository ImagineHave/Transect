from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField
from wtforms.validators import InputRequired
import datetime
from decimal import ROUND_HALF_UP

class EditForm(FlaskForm):
    payer = StringField('payer', [InputRequired()])
    payee = StringField('payee', [InputRequired()])
    amount = DecimalField('amount', [InputRequired()], places=2, default=0.0, rounding=ROUND_HALF_UP)
    date = DateField('date', [InputRequired()], format='%Y-%m-%d')
    submit = SubmitField('edit')