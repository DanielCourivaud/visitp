from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class StreetForm(FlaskForm):
    num = IntegerField('Numéro')
    street = StringField('Voie')
    name = StringField('Nom')
    submit = SubmitField('Save')
