from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired('Fill in this field')])
    name = StringField('Name', validators=[DataRequired('Fill in this field')])
    email = EmailField('Email',
                       validators=[
                           DataRequired('Fill in this field'),
                           Email()
                       ])
    password = PasswordField('Password',
                             validators=[DataRequired('Fill in this field')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                         DataRequired('Fill in this field'),
                                         EqualTo('password')
                                     ])
    button = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired('Fill in this field')])
    password = PasswordField('Password',
                             validators=[DataRequired('Fill in this field')])
    button = SubmitField('Login')
