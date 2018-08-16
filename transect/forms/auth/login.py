from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError
from transect.domain.users import does_password_match_user, get_user_id_from_username


def does_username_exist(form, field):
    if get_user_id_from_username(username=field.data) is None:
        raise ValidationError('username unknown.')


def does_password_match(form, field):
    username = form.username.data
    if not does_password_match_user(username, field.data):
        raise ValidationError('invalid details.')


class LoginForm(FlaskForm):
    username = StringField('username', [validators.InputRequired(), does_username_exist])
    password = PasswordField('password', [validators.InputRequired(), does_password_match])
    submit = SubmitField('login')
