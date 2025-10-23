from flask import Blueprint, render_template, redirect, session,url_for
from wtforms import (SubmitField, SelectField)
from flask_wtf import FlaskForm
from programs.kpis import brands_available, set_channel

brands = brands_available()
class BrandForm(FlaskForm):
    brand = SelectField('Brand', choices=[])
    channel = SelectField('Channel', choices=['SAS Aramis','OPENLANE Deutschland GmbH','B2B'])
    submit = SubmitField('Next')

index_bp = Blueprint('index',
                     __name__,
                     template_folder='../templates')

@index_bp.route("/", methods=["GET", "POST"])                            #HOME
def home():
    form = BrandForm()
    form.brand.choices = [(b, b) for b in brands_available()]

    if form.validate_on_submit():
        session['brand'] = form.brand.data
        session['channel'] = form.channel.data
        return redirect(url_for('model.model'))
    return render_template('index_brand.html', form=form)