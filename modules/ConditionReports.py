from zipfile import ZipFile
import os
import pandas as pd
import requests
import time

def conditionreports(vins):
    session = requests.Session()
    payload = {
        'username': 'c.zorila',
        'password': 'MemoCristian2025'
    }

    try:
        session.post('https://ams-de.mega-moves.com/', data=payload, timeout=15)
    except Exception as e:
        print(f"Login error: {e}")
        return

    df = pd.read_excel('stock_list.xlsx')

    df['FIN'] = df['FIN'].astype(str).str.strip()
    df['Link Gutachten'] = df['Link Gutachten'].astype(str).str.strip()

    pdf_files = []

    for _, row in df.iterrows():
        vin = row['FIN']
        url = row['Link Gutachten']

        if vin not in vins or not url or url == 'nan':
            continue

        try:
            r = session.get(url, timeout=20)
            r.raise_for_status()
            pdf_path = f"{vin}.pdf"
            with open(pdf_path, "wb") as f:
                f.write(r.content)
            pdf_files.append(pdf_path)
            print(f"Downloaded {pdf_path}")
            time.sleep(0.5)  # avoid overloading the server
        except Exception as e:
            print(f"Error downloading {vin}: {e}")

    if not pdf_files:
        print("No valid files downloaded.")
        return

    zip_name = 'ConditionReports.zip'
    try:
        with ZipFile(zip_name, 'w') as zipf:
            for pdf in pdf_files:
                zipf.write(pdf)
    finally:
        for pdf in pdf_files:
            if os.path.exists(pdf):
                os.remove(pdf)

    print(f"Created {zip_name} with {len(pdf_files)} reports.")
