import pandas as pd

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

df = pd.read_excel(r'D:\TradeX\CZ-Learning\TradeX\stock_list.xlsx')
df = df[df['Hersteller'].isin(valid_brands)]
df_sales = pd.read_excel(r'D:\TradeX\CZ-Learning\TradeX\sales_list.xlsx')
df_sales = df_sales[df_sales['VK (Netto)'] > 0]

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

#------------SALES LIST-------------------------------

def units_sold(model):
    units_sales = df_sales['Modell'].value_counts()
    units_sales = units_sales.to_dict()
    return units_sales.get(model, 0)

def average_sell_price(model):
    avg_per_brand = df_sales.groupby('Modell')['VK (Netto)'].mean().round(2)
    avg_dict = avg_per_brand.to_dict()
    return avg_dict.get(model, 0)

#-------------ANALYSIS ON BRAND LEVEL---------------------------------
def stock_per_brand(brand):
    brand_count = df['Hersteller'].value_counts()
    brand_count = brand_count.to_dict()
    return brand_count.get(brand, 0)

def units_sold_brand(brand):
    units_sales = df_sales['Hersteller'].value_counts()
    units_sales = units_sales.to_dict()
    return units_sales.get(brand, 0)

def average_sell_price_brand(brand):
    avg_per_brand = df_sales.groupby('Hersteller')['VK (Netto)'].mean().round(2)
    avg_dict = avg_per_brand.to_dict()
    return avg_dict.get(brand, 0)

#Contries Sold by brand
def countries_sold_brand(brand):
    country_counts = (
        df_sales.loc[df_sales['Hersteller'] == brand, 'Land des Kunden']
        .value_counts()
        .to_dict()
    )
    return country_counts


print(countries_sold_brand('Porsche'))