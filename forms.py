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

    audio = FileField('Audio path', validators=[DataRequired(),FileAllowed(['wav'])])    

    systemName = SelectField('Select System', choices=[('system 0','system 0'),('system 1','system 1'),('system 2','system 2'),
                                                    ('system 3','system 3'),('system 4','system 4')], validate_choice=True)
    systemWeight = SelectField('Select Weight', choices=[('320','320'),('384','384'),('448','448'),('512','512')], validate_choice=True)

    nb_tags = SelectField('nembers of tags', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7')], validate_choice=True) 

    submit = SubmitField('get tags')

class SystemWieght(FlaskForm):
    audio = FileField('Audio path', validators=[DataRequired(),FileAllowed(['wav'])])
    sys2 =  SelectField('System 2 Weight', choices=[('320','320'),('384','384'),('448','448'),('512','512')], validate_choice=True)
    sys3 =  SelectField('System 3 Weight', choices=[('320','320'),('384','384'),('448','448'),('512','512')], validate_choice=True)
    sys4 =  SelectField('System 4 Weight', choices=[('320','320'),('384','384'),('448','448'),('512','512')], validate_choice=True)
    nb_tags = SelectField('nembers of tags', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7')], validate_choice=True)
    submit = SubmitField('get tags') 
  
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

