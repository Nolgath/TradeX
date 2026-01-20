from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class MainPageForm(FlaskForm):
    brand = SelectField('Brand')
    model = SelectField('Model')
    country = SelectField('Country')
    # mileage_from = SelectField('Mileage From')
    # mileage_to = SelectField('Mileage To')
    channel = SelectField('Channel')
    submit = SubmitField('Search')
