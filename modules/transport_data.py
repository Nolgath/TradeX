import pandas as pd
import os

base_path = os.path.dirname(__file__) #Folder where this script is (TradeX_Analysis/modules/calculations.py)
file_path = os.path.join(base_path, '..', 'stock_list.xlsx') #Makes the base_path move a folder back. (Where the Excel file is at)
file_path_sales = os.path.join(base_path, '..', 'sales_list.xlsx') #Makes the base_path move a folder back. (Where the Excel file is at)
stock = pd.read_excel(file_path)
sales = pd.read_excel(file_path_sales)

#Unique vins FIN:
stock_vins = {vin: str(link)[-5:] for vin, link in zip(stock['FIN'], stock['Link Backend'])}
sales_vins = {vin: str(link)[-5:] for vin, link in zip(sales['FIN'], sales['Link'])}
all_vins = {**stock_vins, **sales_vins}

def car_ids(vin):
    vin = str(vin).strip().upper()
    # Fix missing zeros
    if len(vin) < 17:
        vin = vin.zfill(17)
    return all_vins.get(vin)