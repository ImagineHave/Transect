from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField
from wtforms.validators import DataRequired

class AddForm(FlaskForm):
    payer = StringField('payer', [DataRequired()])
    payee = StringField('payee', [DataRequired()])
    amount = DecimalField('amount', [DataRequired()])
    date = DateField('payer', [DataRequired()])
    submit = SubmitField('add')