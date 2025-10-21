from zipfile import ZipFile
import os
import pandas as pd
import requests

def conditionreports(vins):
    # --- LOGIN FIRST ---
    session = requests.Session()
    payload = {
        'username': 'c.zorila',
        'password': 'MemoCristian2025'
    }
    session.post('https://ams-de.mega-moves.com/', data=payload)

    df = pd.read_excel('stock_list.xlsx')

    df['FIN'] = df['FIN'].str.strip()
    df['Link Gutachten'] = df['Link Gutachten'].str.strip()

    vin_list = df['FIN'].to_list()
    condition_url = df['Link Gutachten'].to_list()

    vin_url_pairs = list(zip(vin_list, condition_url))

    pdf_files = []

    for vin, url in vin_url_pairs:
        # Skip if URL is missing, NaN, None, or empty
        if vin not in vins or pd.isna(url) or not isinstance(url, str) or not url.strip():
            continue
        try:
            r = session.get(url)
            r.raise_for_status()  # Raise error for bad status codes (optional)
            with open(f"{vin}.pdf", "wb") as f:
                f.write(r.content)
            pdf_files.append(f"{vin}.pdf")
        except Exception as e:
            print(f"Error downloading VIN {vin}: {e}")

    if pdf_files:
        zip_name = 'ConditionReports.zip'
        with ZipFile(zip_name, 'w') as zipf:
            for pdf in pdf_files:
                zipf.write(pdf)

        for pdf in pdf_files:
            os.remove(pdf)