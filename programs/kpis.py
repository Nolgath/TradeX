import pandas as pd
import os

valid_brands = [
    "Audi","BMW","Mercedes-Benz","Volkswagen","VW","Porsche","Opel","Smart","Maybach",
    "Renault","Peugeot","Citroen","DS Automobiles","Dacia","Bugatti",
    "Fiat","Alfa Romeo","Lancia","Ferrari","Lamborghini","Maserati","Abarth","Pagani",
    "SEAT","Cupra","Skoda",
    "Volvo","Saab","Koenigsegg","Polestar",
    "Mini","Jaguar","Land Rover","Range Rover","Aston Martin","Bentley","Rolls-Royce","McLaren","Lotus",
    "Ford","Chevrolet","GMC","Cadillac","Buick","Chrysler","Dodge","Jeep","Ram","Lincoln",
    "Tesla","Rivian","Lucid","Hummer",
    "Toyota","Lexus","Honda","Acura","Nissan","Infiniti","Mazda","Mitsubishi","Subaru","Suzuki","Daihatsu","Isuzu",
    "Hyundai","Kia","Genesis",
    "BYD","Geely","Great Wall","Chery","MG","NIO","Xpeng","Lynk & Co","Ora","Zeekr",
    "Tata","Mahindra",
    "Iveco","MAN","Scania","DAF","Renault Trucks","Volvo Trucks","Mercedes-Benz Vans","Ford Trucks"
]

base_path = os.path.dirname(os.path.abspath(__file__))
stock_path = os.path.join(base_path, "..", "stock_list.xlsx")
sales_path = os.path.join(base_path, "..", "sales_list.xlsx")
df = pd.read_excel(stock_path)
df = df[df['Hersteller'].isin(valid_brands)]
df_sales = pd.read_excel(sales_path)
df_sales = df_sales[df_sales['VK (Netto)'] > 0]

channel_value = None
exclude_channels = []

def set_channel(value):
    global channel_value, exclude_channels
    channel_value = value
    exclude_channels = ['SAS Aramis', 'OPENLANE Deutschland GmbH'] if value == 'B2B' else []


#------------STOCK LIST-------------------------------
def brands_available():
    brands_list = df['Hersteller'].unique()
    brands_list.tolist()
    return brands_list

#---Models gets selected for the brand selected
def models_available(brand):
    models = df.loc[df['Hersteller'] == brand, 'Modell'].unique()
    return models.tolist()

def stock_per_model(model):
    brand_count = df['Modell'].value_counts()
    brand_count = brand_count.to_dict()
    return brand_count.get(model, 0)

def stock_per_brand(brand):
    brand_count = df['Hersteller'].value_counts()
    brand_count = brand_count.to_dict()
    return brand_count.get(brand, 0)


#------------SALES LIST-------------------------------

def units_sold(model):
    if channel_value == 'B2B':
        filtered = df_sales[
            (df_sales['Modell'] == model) &
            (~df_sales['Kunde'].isin(exclude_channels))
        ]
    else:
        filtered = df_sales[
            (df_sales['Modell'] == model) &
            (df_sales['Kunde'] == channel_value)
        ]
    return len(filtered)

def average_sell_price(model):
    if channel_value == 'B2B':
        filtered = df_sales[
            (df_sales['Modell'] == model) &
            (~df_sales['Kunde'].isin(exclude_channels))
        ]
    else:
        filtered = df_sales[
            (df_sales['Modell'] == model) &
            (df_sales['Kunde'] == channel_value)
        ]

    if filtered.empty:
        return 0
    return round(filtered['VK (Netto)'].mean(), 2)


#-------------ANALYSIS ON BRAND LEVEL---------------------------------

def units_sold_brand(brand):
    if channel_value == 'B2B':
        filtered = df_sales[
            (df_sales['Hersteller'] == brand) &
            (~df_sales['Kunde'].isin(exclude_channels))
        ]
    else:
        filtered = df_sales[
            (df_sales['Hersteller'] == brand) &
            (df_sales['Kunde'] == channel_value)
        ]

    return len(filtered)


def average_sell_price_brand(brand):
    if channel_value == 'B2B':
        filtered = df_sales[
            (df_sales['Hersteller'] == brand) &
            (~df_sales['Kunde'].isin(exclude_channels))
        ]
    else:
        filtered = df_sales[
            (df_sales['Hersteller'] == brand) &
            (df_sales['Kunde'] == channel_value)
        ]

    if filtered.empty:
        return 0
    return round(filtered['VK (Netto)'].mean(), 2)


#Contries Sold by brand
def countries_sold_brand(brand):
    if channel_value == 'B2B':
        filtered = df_sales[
            (df_sales['Hersteller'] == brand) &
            (~df_sales['Kunde'].isin(exclude_channels))
        ]
    else:
        filtered = df_sales[
            (df_sales['Hersteller'] == brand) &
            (df_sales['Kunde'] == channel_value)
        ]

    country_counts = filtered['Land des Kunden'].value_counts().to_dict()
    return country_counts


#Contries Sold by brand
def countries_sold_model(model):
    if channel_value == 'B2B':
        filtered = df_sales[
            (df_sales['Modell'] == model) &
            (~df_sales['Kunde'].isin(exclude_channels))
        ]
    else:
        filtered = df_sales[
            (df_sales['Modell'] == model) &
            (df_sales['Kunde'] == channel_value)
        ]

    country_counts = filtered['Land des Kunden'].value_counts().to_dict()
    return country_counts
