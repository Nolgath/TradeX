from flask import Blueprint, render_template, request
from modules.forms import MainPageForm
from modules.calculations import (brands_available,models_available,cars_in_stock,cars_sold,total_revenue,total_profit,channels_available,
                                  sell_through_rate,average_purchasing_price,average_margin,average_selling_price,set_channel, average_mileage)
main_page_bp = Blueprint("main_page", __name__)
@main_page_bp.route("/", methods=["GET", "POST"])
def main_page():
    form = MainPageForm()
    form.brand.choices = [("", "Select brand")] + brands_available()
    form.model.choices = [("", "Select model")]

    model = None
    channel= None
    display_model = False
    display_channel = False
    display_results = False

    if request.method == "POST":
        brand = request.form.get("brand")
        model = request.form.get("model")
        channel = request.form.get("channel")

        if brand:
            form.model.choices = [("", "Select model")] + models_available(brand)
            display_model = True
        if model:
            display_channel = True
            form.channel.choices = channels_available(model)
        if channel:
            display_results = True

    set_channel_calc = set_channel(channel)
    cars_in_stock_calc = cars_in_stock(model)
    cars_sold_calc = cars_sold(model)
    sell_through_rate_calc = sell_through_rate(model)
    average_purchasing_price_calc = average_purchasing_price(model)
    average_selling_price_calc = average_selling_price(model)
    average_margin_calc = average_margin(model)
    total_revenue_calc = total_revenue(model)
    total_profit_calc = total_profit(model)
    average_mileage_calc = average_mileage(model)

    return render_template(
        "analysis_page.html",
        form=form, display_model=display_model, display_results=display_results,
        display_channel=display_channel, cars_in_stock_calc=cars_in_stock_calc, cars_sold_calc=cars_sold_calc,
        sell_through_rate_calc=sell_through_rate_calc, average_purchasing_price_calc=average_purchasing_price_calc,
        average_selling_price_calc=average_selling_price_calc, average_margin_calc=average_margin_calc,total_revenue_calc=total_revenue_calc,
        total_profit_calc=total_profit_calc,set_channel_calc=set_channel_calc,average_mileage_calc=average_mileage_calc
    )