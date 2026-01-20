import os
import pandas as pd

#Sales are last 30 days.

base_path = os.path.dirname(__file__) #Folder where this script is (TradeX_Analysis/modules/calculations.py)
file_path = os.path.join(base_path, '..', 'stock_list.xlsx') #Makes the base_path move a folder back. (Where the Excel file is at)
file_path_sales = os.path.join(base_path, '..', 'sales_list.xlsx') #Makes the base_path move a folder back. (Where the Excel file is at)
stock = pd.read_excel(file_path)
sales = pd.read_excel(file_path_sales)
sales = sales[sales['VK (Netto)'] > 0]
keep = ['SAS Aramis', 'OPENLANE Deutschland GmbH']
sales['Kunde'] = sales['Kunde'].where(sales['Kunde'].isin(keep), 'B2B')

#------- CHANNEL SELECTION -------
channel_value = None

def set_channel(value): #Set active channel
    global channel_value
    channel_value = value

def channels_available(model):
    channels = sales.loc[sales['Modell'] == model, 'Kunde'].unique().tolist()
    if not channels:
        return ['None Sold']
    return [(c, c) for c in channels]

#------- CAR SELECTION -----
def brands_available(): #Select Brands
    unique_brands = stock['Hersteller'].unique().tolist()
    unique_brands = [(brand, brand) for brand in unique_brands]
    return unique_brands

def models_available(brand): #Select Models according to brand selected
    unique_models = stock[stock['Hersteller'] == brand]['Modell'].unique().tolist()
    unique_models = [(model, model) for model in unique_models]
    return unique_models

#------- OVERVIEW CALCULATIONS -----
def cars_in_stock(model): #Nº of cars in stock
    return stock[stock['Modell'] == model].shape[0]

def cars_sold(model): #Nº of cars sold
    return sales[(sales['Modell'] == model) & (sales['Kunde'] == channel_value)].shape[0]

def sell_through_rate(model): #Sell-through rate (%)
    stock_quantity = cars_in_stock(model)
    sales_quantity = cars_sold(model)
    if stock_quantity == 0:
        return "N/A"
    sell_through_rate_calc = sales_quantity / stock_quantity * 100
    return f"{int(sell_through_rate_calc)}%"

#------- PRICING CALCULATIONS -----
def average_selling_price(model): #Average selling price (€)
    filtered = sales[(sales['Modell'] == model) & (sales['Kunde'] == channel_value)]
    mean_val = filtered['VK (Netto)'].mean()
    if pd.isna(mean_val):
        return "N/A"
    return int(mean_val)

def average_purchasing_price(model): #Average purchasing price (€)
    filtered = sales[(sales['Modell'] == model) & (sales['Kunde'] == channel_value)]
    mean_val = filtered['EK (Netto)'].mean()
    if pd.isna(mean_val):
        return "N/A"
    return int(mean_val)

def average_margin(model): #Average margin (€)
    avg_sell_price = average_selling_price(model)
    avg_purchase_price = average_purchasing_price(model)
    if avg_sell_price == "N/A" or avg_purchase_price == "N/A":
        return "N/A"
    margin = int(avg_sell_price) - int(avg_purchase_price)
    return int(margin)

#------- PROFITABILITY CALCULATIONS -----
def total_revenue(model): #Total revenue
    filtered = sales[(sales['Modell'] == model) & (sales['Kunde'] == channel_value)]
    total_rev = filtered['VK (Netto)'].sum()
    if pd.isna(total_rev) or total_rev == 0:
        return "N/A"
    return int(total_rev)


def total_profit(model): #Total profit
    filtered = sales[(sales['Modell'] == model) & (sales['Kunde'] == channel_value)]
    total_prof = filtered['DB (Fahrzeug)'].sum()
    if pd.isna(total_prof) or total_prof == 0:
        return "N/A"
    return int(total_prof)

#------- STOCK INSIGHTS CALCULATIONS -----
def average_stock_age(): #Average stock age (days)
    pass

def average_mileage(model):
    mileage = stock[stock['Modell'] == model]['km'].mean()
    if pd.isna(mileage):
        return "N/A"
    return int(mileage)

def cars_with_damages():
    pass

# def country_sold(brand,model):
#     unique_countries = sales[(sales['Hersteller']==brand)&(sales['Modell']==model)]['Land des Kunde'].unique().tolist()
#     unique_countries = [(country, country) for country in unique_countries]
#     return unique_countries
