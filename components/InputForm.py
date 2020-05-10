from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class InputForm(FlaskForm):
    command = StringField('Select your command: ')
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')
