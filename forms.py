from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, DataRequired

class GetTagsForm(FlaskForm):
    audio = FileField('Audio path', validators=[DataRequired(),FileAllowed(['wav'])])
    submit = SubmitField('get tags')