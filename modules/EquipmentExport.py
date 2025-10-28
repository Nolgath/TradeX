import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO

def equipment_export(vins):
    # --- LOGIN FIRST ---
    session = requests.Session()
    payload = {
        'username': 'c.zorila',
        'password': 'MemoCristian2025'
    }
    session.post('https://ams-de.mega-moves.com/', data=payload)

    df = pd.read_excel('stock_list.xlsx')

    df['FIN'] = (df['FIN'].astype(str).str.upper().str.strip().str.replace(r'\s+', '', regex=True))
    df['Link Backend'] = df['Link Backend'].str.strip()

    vin_url_pairs = list(zip(df['FIN'], df['Link Backend']))

    equipment_list = []

    for vin, url in vin_url_pairs:
        if vin in vins:
            resp = session.get(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            equipment = soup.select_one('#tradex_equipment')
            equipment_text = equipment.get('value','').strip()
            equipment_list.append({"VIN": vin, "Equipment": equipment_text})
            print(f"VIN: {vin}, Equipment: {equipment_text}")

    # Create dataframe
    result_df = pd.DataFrame(equipment_list)

    # Write to BytesIO (in-memory file)
    output = BytesIO()
    result_df.to_excel(output, index=False)
    output.seek(0)
    return output