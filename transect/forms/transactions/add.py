from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, 
from wtforms.fields.html5 import DateField

class AddForm(FlaskForm):
    payer = StringField('payer', [validators.DataRequired()])
    payee = StringField('payee', [validators.DataRequired()])
    amount = DecimalField('amount', [validators.DataRequired()])
    date = DateField('payer', [validators.DataRequired()])
    submit = SubmitField('add')