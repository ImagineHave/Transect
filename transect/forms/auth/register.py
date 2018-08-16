from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from transect.domain.users import get_user_id_from_username


def does_username_exist(username):
    if get_user_id_from_username(username=username) is not None:
        raise ValidationError('Username already used')


class RegisterForm(FlaskForm):
    email = StringField('email', [DataRequired("email address required."), Email("email address required.")])
    username = StringField('username', validators=[DataRequired("username required."), does_username_exist])
    password = PasswordField('password', [
        DataRequired("password required."),
        EqualTo('confirm', message='passwords must match.')
    ])
    confirm = PasswordField('confirm password')
    submit = SubmitField('register')

