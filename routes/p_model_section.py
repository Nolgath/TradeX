from flask import Blueprint, render_template, redirect, session,url_for
from wtforms import (SubmitField, SelectField)
from flask_wtf import FlaskForm
from programs.kpis import (models_available,stock_per_brand,
                           units_sold_brand, average_sell_price_brand,countries_sold_brand)

class ModelForm(FlaskForm):
    model = SelectField('Model', choices=[])
    submit = SubmitField('See Results')

model_bp = Blueprint('model',
                     __name__,
                     template_folder='../templates')

@model_bp.route("/model",methods=["GET","POST"])                         #MODEL
def model():
    brand = session.get('brand')  # get selected brand
    form = ModelForm()
    form.model.choices = [(m, m) for m in models_available(brand)]


    country_sold = countries_sold = countries_sold_brand(brand)
    stock_p_brand = stock_per_brand(brand)
    units_sold_p_brand = units_sold_brand(brand)
    average_sell_price_p_brand = average_sell_price_brand(brand)

    if form.validate_on_submit():
        session['model'] = form.model.data
        return redirect(url_for('analysis.analysis'))
    return render_template('index_model.html', form=form, brand=brand,
                           stock_p_brand=stock_p_brand,units_sold_p_brand=units_sold_p_brand,
                           average_sell_price_p_brand=average_sell_price_p_brand,
                           country_sold=country_sold)