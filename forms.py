from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from flask_wtf.file import FileField, FileAllowed, DataRequired
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class GetTagsForm(FlaskForm):
    audio = FileField('Audio path', validators=[DataRequired(),FileAllowed(['wav'])])
    submit = SubmitField('get tags')

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

