from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators

class LoginForm(FlaskForm):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.DataRequired()])
    submit = SubmitField('login')