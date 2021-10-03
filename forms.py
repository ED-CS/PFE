from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, SelectField
from flask_wtf.file import FileField, FileAllowed, DataRequired
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class GetTagsForm(FlaskForm):
    audio = FileField('Audio path', validators=[DataRequired(),FileAllowed(['wav'])])
    nb_tags = SelectField('nembers of tags', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7')])
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
                                                    ('system 3','system 3'),('system 4','system 4')])                                 
    systemWeight = SelectField('Select Weight', choices=[('320','320'),('384','384'),('448','448'),('512','512')])

    nb_tags = SelectField('nembers of tags', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7')]) 

    submit = SubmitField('get tags')
["RestNet 1", "ResNet 2", "RestNet 1 + PL", "RestNet 1 + PL + MT", "RestNet 2 + PL + MT"]
class SystemWieght(FlaskForm):
    audio = FileField('Audio path', validators=[DataRequired(),FileAllowed(['wav'])])
    sys2 =  SelectField('RestNet 1 + PL', choices=[('320','320'),('384','384'),('448','448'),('512','512')])
    sys3 =  SelectField('RestNet 1 + PL + MT', choices=[('320','320'),('384','384'),('448','448'),('512','512')])
    sys4 =  SelectField('RestNet 2 + PL + MT', choices=[('320','320'),('384','384'),('448','448'),('512','512')])
    nb_tags = SelectField('nembers of tags', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7')])
    submit = SubmitField('get tags') 
  
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

