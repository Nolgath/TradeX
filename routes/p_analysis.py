from flask import Blueprint, render_template, session
from programs.kpis import stock_per_model,units_sold,average_sell_price,countries_sold_model

analysis_bp = Blueprint('analysis',
                        __name__,
                        template_folder='templates')

@analysis_bp.route("/analysis",methods=["GET","POST"])
def analysis():
    brand = session.get('brand')
    model = session.get('model')
    channel = session.get('channel')

    countries_sold = countries_sold_model(model)
    stock_count = stock_per_model(model) #number of cars with this model
    sold_units = units_sold(model) #units sold per this model
    avg_sell_price = average_sell_price(model) #average selling price per this model

    return render_template('analysis.html',
                           brand=brand, model=model,
                           stock_count=stock_count,sold_units=sold_units,
                           avg_sell_price=avg_sell_price,
                           countries_sold=countries_sold)