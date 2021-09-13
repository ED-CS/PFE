from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, SelectField
from flask_wtf.file import FileField, FileAllowed, DataRequired
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class GetTagsForm(FlaskForm):
    audio = FileField('Audio path', validators=[DataRequired(),FileAllowed(['wav'])])
    nb_tags = SelectField('nembers of tags', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7')], validate_choice=True)
    submit = SubmitField('get tags')

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create account')
class SystemOptionForm(FlaskForm):
    system = SelectField('Select System', choices=[('System 0','System 0'),('System 1','System 1'),('System 2','System 2'),
                                                    ('System 3','System 3'),('System 4','System 4')], validate_choice=True)
    submit = SubmitField('get tags')
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

