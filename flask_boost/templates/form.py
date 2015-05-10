# coding: utf-8
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class ExampleForm(Form):
    field = StringField('', validators=[DataRequired()])
