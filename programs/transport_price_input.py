import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from playwright.sync_api import sync_playwright

def transport_price_input(vins,slot,value):
    session = requests.Session()
    payload = {
        'username': 'c.zorila',
        'password': 'MemoCristian2025'
    }
    session.post('https://ams-de.mega-moves.com/', data=payload)

    df = pd.read_excel('stock_list.xlsx')
    df['FIN'] = (df['FIN'].astype(str).str.upper().str.strip().str.replace(r'\s+', '', regex=True))
    df['Link Backend'] = df['Link Backend'].str.strip()
    df['id'] = df['Link Backend'].str[-5:]

    vin_url_pairs = list(zip(df['FIN'], df['id']))

    list_payments = []

    for vin, id in vin_url_pairs:
        if vin in vins:
            web_url = 'https://ams-de.mega-moves.com/portal/vehicles/pages/vehicle-details-5.php?wgID='+id
            print(web_url)
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                page.goto(web_url)
                page.fill("input[name=username]", payload['username'])
                page.fill("input[name=password]", payload['password'])
                page.click("button[type=submit]")
                page.goto(web_url)

                #start inputs


vins = ['WVGZZZ1TZMW009416']
transport_price_input(vins,4,1000)
